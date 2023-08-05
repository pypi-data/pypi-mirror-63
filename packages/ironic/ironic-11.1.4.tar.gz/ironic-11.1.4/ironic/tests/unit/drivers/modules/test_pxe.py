# Copyright 2013 Hewlett-Packard Development Company, L.P.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""Test class for PXE driver."""

import os
import tempfile

from ironic_lib import utils as ironic_utils
import mock
from oslo_config import cfg
from oslo_serialization import jsonutils as json
from oslo_utils import fileutils
from oslo_utils import uuidutils

from ironic.common import boot_devices
from ironic.common import boot_modes
from ironic.common import dhcp_factory
from ironic.common import exception
from ironic.common.glance_service import base_image_service
from ironic.common import pxe_utils
from ironic.common import states
from ironic.common import utils as common_utils
from ironic.conductor import task_manager
from ironic.conductor import utils as manager_utils
from ironic.drivers import base as drivers_base
from ironic.drivers.modules import agent_base_vendor
from ironic.drivers.modules import deploy_utils
from ironic.drivers.modules import pxe
from ironic.drivers.modules.storage import noop as noop_storage
from ironic.tests.unit.db import base as db_base
from ironic.tests.unit.db import utils as db_utils
from ironic.tests.unit.objects import utils as obj_utils

CONF = cfg.CONF

INST_INFO_DICT = db_utils.get_test_pxe_instance_info()
DRV_INFO_DICT = db_utils.get_test_pxe_driver_info()
DRV_INTERNAL_INFO_DICT = db_utils.get_test_pxe_driver_internal_info()


@mock.patch.object(pxe.PXEBoot, '__init__', lambda self: None)
class PXEPrivateMethodsTestCase(db_base.DbTestCase):

    def setUp(self):
        super(PXEPrivateMethodsTestCase, self).setUp()
        n = {
            'driver': 'fake-hardware',
            'boot_interface': 'pxe',
            'instance_info': INST_INFO_DICT,
            'driver_info': DRV_INFO_DICT,
            'driver_internal_info': DRV_INTERNAL_INFO_DICT,
        }
        self.config_temp_dir('http_root', group='deploy')
        self.node = obj_utils.create_test_node(self.context, **n)

    def _test__parse_driver_info_missing_kernel(self, mode='deploy'):
        del self.node.driver_info['%s_kernel' % mode]
        if mode == 'rescue':
            self.node.provision_state = states.RESCUING
        self.assertRaises(exception.MissingParameterValue,
                          pxe._parse_driver_info, self.node, mode=mode)

    def test__parse_driver_info_missing_deploy_kernel(self):
        self._test__parse_driver_info_missing_kernel()

    def test__parse_driver_info_missing_rescue_kernel(self):
        self._test__parse_driver_info_missing_kernel(mode='rescue')

    def _test__parse_driver_info_missing_ramdisk(self, mode='deploy'):
        del self.node.driver_info['%s_ramdisk' % mode]
        if mode == 'rescue':
            self.node.provision_state = states.RESCUING
        self.assertRaises(exception.MissingParameterValue,
                          pxe._parse_driver_info, self.node, mode=mode)

    def test__parse_driver_info_missing_deploy_ramdisk(self):
        self._test__parse_driver_info_missing_ramdisk()

    def test__parse_driver_info_missing_rescue_ramdisk(self):
        self._test__parse_driver_info_missing_ramdisk(mode='rescue')

    def _test__parse_driver_info(self, mode='deploy'):
        exp_info = {'%s_ramdisk' % mode: 'glance://%s_ramdisk_uuid' % mode,
                    '%s_kernel' % mode: 'glance://%s_kernel_uuid' % mode}
        image_info = pxe._parse_driver_info(self.node, mode=mode)
        self.assertEqual(exp_info, image_info)

    def test__parse_driver_info_deploy(self):
        self._test__parse_driver_info()

    def test__parse_driver_info_rescue(self):
        self._test__parse_driver_info(mode='rescue')

    def test__get_deploy_image_info(self):
        expected_info = {'deploy_ramdisk':
                         (DRV_INFO_DICT['deploy_ramdisk'],
                          os.path.join(CONF.pxe.tftp_root,
                                       self.node.uuid,
                                       'deploy_ramdisk')),
                         'deploy_kernel':
                         (DRV_INFO_DICT['deploy_kernel'],
                          os.path.join(CONF.pxe.tftp_root,
                                       self.node.uuid,
                                       'deploy_kernel'))}
        image_info = pxe._get_image_info(self.node)
        self.assertEqual(expected_info, image_info)

    def test__get_deploy_image_info_missing_deploy_kernel(self):
        del self.node.driver_info['deploy_kernel']
        self.assertRaises(exception.MissingParameterValue,
                          pxe._get_image_info, self.node)

    def test__get_deploy_image_info_deploy_ramdisk(self):
        del self.node.driver_info['deploy_ramdisk']
        self.assertRaises(exception.MissingParameterValue,
                          pxe._get_image_info, self.node)

    @mock.patch.object(base_image_service.BaseImageService, '_show',
                       autospec=True)
    def _test__get_instance_image_info(self, show_mock):
        properties = {'properties': {u'kernel_id': u'instance_kernel_uuid',
                      u'ramdisk_id': u'instance_ramdisk_uuid'}}

        expected_info = {'ramdisk':
                         ('instance_ramdisk_uuid',
                          os.path.join(CONF.pxe.tftp_root,
                                       self.node.uuid,
                                       'ramdisk')),
                         'kernel':
                         ('instance_kernel_uuid',
                          os.path.join(CONF.pxe.tftp_root,
                                       self.node.uuid,
                                       'kernel'))}
        show_mock.return_value = properties
        self.context.auth_token = 'fake'
        image_info = pxe._get_instance_image_info(self.node, self.context)
        show_mock.assert_called_once_with(mock.ANY, 'glance://image_uuid',
                                          method='get')
        self.assertEqual(expected_info, image_info)

        # test with saved info
        show_mock.reset_mock()
        image_info = pxe._get_instance_image_info(self.node, self.context)
        self.assertEqual(expected_info, image_info)
        self.assertFalse(show_mock.called)
        self.assertEqual('instance_kernel_uuid',
                         self.node.instance_info['kernel'])
        self.assertEqual('instance_ramdisk_uuid',
                         self.node.instance_info['ramdisk'])

    def test__get_instance_image_info(self):
        # Tests when 'is_whole_disk_image' exists in driver_internal_info
        self._test__get_instance_image_info()

    def test__get_instance_image_info_without_is_whole_disk_image(self):
        # Tests when 'is_whole_disk_image' doesn't exists in
        # driver_internal_info
        del self.node.driver_internal_info['is_whole_disk_image']
        self.node.save()
        self._test__get_instance_image_info()

    @mock.patch('ironic.drivers.modules.deploy_utils.get_boot_option',
                return_value='local')
    def test__get_instance_image_info_localboot(self, boot_opt_mock):
        self.node.driver_internal_info['is_whole_disk_image'] = False
        self.node.save()
        image_info = pxe._get_instance_image_info(self.node, self.context)
        self.assertEqual({}, image_info)
        boot_opt_mock.assert_called_once_with(self.node)

    @mock.patch.object(base_image_service.BaseImageService, '_show',
                       autospec=True)
    def test__get_instance_image_info_whole_disk_image(self, show_mock):
        properties = {'properties': None}
        show_mock.return_value = properties
        self.node.driver_internal_info['is_whole_disk_image'] = True
        image_info = pxe._get_instance_image_info(self.node, self.context)
        self.assertEqual({}, image_info)

    @mock.patch('ironic.common.utils.render_template', autospec=True)
    def _test_build_pxe_config_options_pxe(self, render_mock,
                                           whle_dsk_img=False,
                                           debug=False, mode='deploy'):
        self.config(debug=debug)
        self.config(pxe_append_params='test_param', group='pxe')
        # NOTE: right '/' should be removed from url string
        self.config(api_url='http://192.168.122.184:6385', group='conductor')

        driver_internal_info = self.node.driver_internal_info
        driver_internal_info['is_whole_disk_image'] = whle_dsk_img
        self.node.driver_internal_info = driver_internal_info
        self.node.save()

        tftp_server = CONF.pxe.tftp_server

        kernel_label = '%s_kernel' % mode
        ramdisk_label = '%s_ramdisk' % mode

        pxe_kernel = os.path.join(self.node.uuid, kernel_label)
        pxe_ramdisk = os.path.join(self.node.uuid, ramdisk_label)
        kernel = os.path.join(self.node.uuid, 'kernel')
        ramdisk = os.path.join(self.node.uuid, 'ramdisk')
        root_dir = CONF.pxe.tftp_root

        image_info = {
            kernel_label: (kernel_label,
                           os.path.join(root_dir,
                                        self.node.uuid,
                                        kernel_label)),
            ramdisk_label: (ramdisk_label,
                            os.path.join(root_dir,
                                         self.node.uuid,
                                         ramdisk_label))
        }

        if (whle_dsk_img
            or deploy_utils.get_boot_option(self.node) == 'local'):
                ramdisk = 'no_ramdisk'
                kernel = 'no_kernel'
        else:
            image_info.update({
                'kernel': ('kernel_id',
                           os.path.join(root_dir,
                                        self.node.uuid,
                                        'kernel')),
                'ramdisk': ('ramdisk_id',
                            os.path.join(root_dir,
                                         self.node.uuid,
                                         'ramdisk'))
            })

        expected_pxe_params = 'test_param'
        if debug:
            expected_pxe_params += ' ipa-debug=1'

        expected_options = {
            'deployment_ari_path': pxe_ramdisk,
            'pxe_append_params': expected_pxe_params,
            'deployment_aki_path': pxe_kernel,
            'tftp_server': tftp_server,
            'ipxe_timeout': 0,
            'ari_path': ramdisk,
            'aki_path': kernel,
        }

        if mode == 'rescue':
            self.node.provision_state = states.RESCUING
            self.node.save()

        with task_manager.acquire(self.context, self.node.uuid,
                                  shared=True) as task:
            options = pxe._build_pxe_config_options(task, image_info)
        self.assertEqual(expected_options, options)

    def test__build_pxe_config_options_pxe(self):
        self._test_build_pxe_config_options_pxe(whle_dsk_img=True)

    def test__build_pxe_config_options_pxe_ipa_debug(self):
        self._test_build_pxe_config_options_pxe(debug=True)

    def test__build_pxe_config_options_pxe_rescue(self):
        del self.node.driver_internal_info['is_whole_disk_image']
        self._test_build_pxe_config_options_pxe(mode='rescue')

    def test__build_pxe_config_options_ipa_debug_rescue(self):
        del self.node.driver_internal_info['is_whole_disk_image']
        self._test_build_pxe_config_options_pxe(debug=True, mode='rescue')

    def test__build_pxe_config_options_pxe_local_boot(self):
        del self.node.driver_internal_info['is_whole_disk_image']
        i_info = self.node.instance_info
        i_info.update({'capabilities': {'boot_option': 'local'}})
        self.node.instance_info = i_info
        self.node.save()
        self._test_build_pxe_config_options_pxe(whle_dsk_img=False)

    def test__build_pxe_config_options_pxe_without_is_whole_disk_image(self):
        del self.node.driver_internal_info['is_whole_disk_image']
        self.node.save()
        self._test_build_pxe_config_options_pxe(whle_dsk_img=False)

    def test__build_pxe_config_options_pxe_no_kernel_no_ramdisk(self):
        del self.node.driver_internal_info['is_whole_disk_image']
        self.node.save()
        pxe_params = 'my-pxe-append-params ipa-debug=0'
        self.config(group='pxe', tftp_server='my-tftp-server')
        self.config(group='pxe', pxe_append_params=pxe_params)
        self.config(group='pxe', tftp_root='/tftp-path/')
        image_info = {
            'deploy_kernel': ('deploy_kernel',
                              os.path.join(CONF.pxe.tftp_root,
                                           'path-to-deploy_kernel')),
            'deploy_ramdisk': ('deploy_ramdisk',
                               os.path.join(CONF.pxe.tftp_root,
                                            'path-to-deploy_ramdisk'))}

        with task_manager.acquire(self.context, self.node.uuid,
                                  shared=True) as task:
            options = pxe._build_pxe_config_options(task, image_info)

        expected_options = {
            'deployment_aki_path': 'path-to-deploy_kernel',
            'deployment_ari_path': 'path-to-deploy_ramdisk',
            'pxe_append_params': pxe_params,
            'tftp_server': 'my-tftp-server',
            'aki_path': 'no_kernel',
            'ari_path': 'no_ramdisk',
            'ipxe_timeout': 0}
        self.assertEqual(expected_options, options)

    @mock.patch('ironic.common.image_service.GlanceImageService',
                autospec=True)
    @mock.patch('ironic.common.utils.render_template', autospec=True)
    def _test_build_pxe_config_options_ipxe(self, render_mock, glance_mock,
                                            whle_dsk_img=False,
                                            ipxe_timeout=0,
                                            ipxe_use_swift=False,
                                            debug=False,
                                            boot_from_volume=False,
                                            mode='deploy'):
        self.config(debug=debug)
        self.config(pxe_append_params='test_param', group='pxe')
        # NOTE: right '/' should be removed from url string
        self.config(api_url='http://192.168.122.184:6385', group='conductor')
        self.config(ipxe_timeout=ipxe_timeout, group='pxe')
        root_dir = CONF.deploy.http_root

        driver_internal_info = self.node.driver_internal_info
        driver_internal_info['is_whole_disk_image'] = whle_dsk_img
        self.node.driver_internal_info = driver_internal_info
        self.node.save()

        tftp_server = CONF.pxe.tftp_server

        http_url = 'http://192.1.2.3:1234'
        self.config(ipxe_enabled=True, group='pxe')
        self.config(http_url=http_url, group='deploy')

        kernel_label = '%s_kernel' % mode
        ramdisk_label = '%s_ramdisk' % mode

        if ipxe_use_swift:
            self.config(ipxe_use_swift=True, group='pxe')
            glance = mock.Mock()
            glance_mock.return_value = glance
            glance.swift_temp_url.side_effect = [
                pxe_kernel, pxe_ramdisk] = [
                'swift_kernel', 'swift_ramdisk']
            image_info = {
                kernel_label: (uuidutils.generate_uuid(),
                               os.path.join(root_dir,
                                            self.node.uuid,
                                            kernel_label)),
                ramdisk_label: (uuidutils.generate_uuid(),
                                os.path.join(root_dir,
                                             self.node.uuid,
                                             ramdisk_label))
            }
        else:
            pxe_kernel = os.path.join(http_url, self.node.uuid,
                                      kernel_label)
            pxe_ramdisk = os.path.join(http_url, self.node.uuid,
                                       ramdisk_label)
            image_info = {
                kernel_label: (kernel_label,
                               os.path.join(root_dir,
                                            self.node.uuid,
                                            kernel_label)),
                ramdisk_label: (ramdisk_label,
                                os.path.join(root_dir,
                                             self.node.uuid,
                                             ramdisk_label))
            }

        kernel = os.path.join(http_url, self.node.uuid, 'kernel')
        ramdisk = os.path.join(http_url, self.node.uuid, 'ramdisk')
        if (whle_dsk_img
            or deploy_utils.get_boot_option(self.node) == 'local'):
                ramdisk = 'no_ramdisk'
                kernel = 'no_kernel'
        else:
            image_info.update({
                'kernel': ('kernel_id',
                           os.path.join(root_dir,
                                        self.node.uuid,
                                        'kernel')),
                'ramdisk': ('ramdisk_id',
                            os.path.join(root_dir,
                                         self.node.uuid,
                                         'ramdisk'))
            })

        ipxe_timeout_in_ms = ipxe_timeout * 1000

        expected_pxe_params = 'test_param'
        if debug:
            expected_pxe_params += ' ipa-debug=1'

        expected_options = {
            'deployment_ari_path': pxe_ramdisk,
            'pxe_append_params': expected_pxe_params,
            'deployment_aki_path': pxe_kernel,
            'tftp_server': tftp_server,
            'ipxe_timeout': ipxe_timeout_in_ms,
            'ari_path': ramdisk,
            'aki_path': kernel,
            'initrd_filename': ramdisk_label,
        }

        if mode == 'rescue':
            self.node.provision_state = states.RESCUING
            self.node.save()

        if boot_from_volume:
            expected_options.update({
                'boot_from_volume': True,
                'iscsi_boot_url': 'iscsi:fake_host::3260:0:fake_iqn',
                'iscsi_initiator_iqn': 'fake_iqn_initiator',
                'iscsi_volumes': [{'url': 'iscsi:fake_host::3260:1:fake_iqn',
                                   'username': 'fake_username_1',
                                   'password': 'fake_password_1'
                                   }],
                'username': 'fake_username',
                'password': 'fake_password'
            })
            expected_options.pop('deployment_aki_path')
            expected_options.pop('deployment_ari_path')
            expected_options.pop('initrd_filename')

        with task_manager.acquire(self.context, self.node.uuid,
                                  shared=True) as task:
            options = pxe._build_pxe_config_options(task, image_info)
        self.assertEqual(expected_options, options)

    def test__build_pxe_config_options_ipxe(self):
        self._test_build_pxe_config_options_ipxe(whle_dsk_img=True)

    def test__build_pxe_config_options_ipxe_ipa_debug(self):
        self._test_build_pxe_config_options_ipxe(debug=True)

    def test__build_pxe_config_options_ipxe_local_boot(self):
        del self.node.driver_internal_info['is_whole_disk_image']
        i_info = self.node.instance_info
        i_info.update({'capabilities': {'boot_option': 'local'}})
        self.node.instance_info = i_info
        self.node.save()
        self._test_build_pxe_config_options_ipxe(whle_dsk_img=False)

    def test__build_pxe_config_options_ipxe_swift_wdi(self):
        self._test_build_pxe_config_options_ipxe(whle_dsk_img=True,
                                                 ipxe_use_swift=True)

    def test__build_pxe_config_options_ipxe_swift_partition(self):
        self._test_build_pxe_config_options_ipxe(whle_dsk_img=False,
                                                 ipxe_use_swift=True)

    def test__build_pxe_config_options_ipxe_and_ipxe_timeout(self):
        self._test_build_pxe_config_options_ipxe(whle_dsk_img=True,
                                                 ipxe_timeout=120)

    def test__build_pxe_config_options_ipxe_and_iscsi_boot(self):
        vol_id = uuidutils.generate_uuid()
        vol_id2 = uuidutils.generate_uuid()
        obj_utils.create_test_volume_connector(
            self.context,
            uuid=uuidutils.generate_uuid(),
            type='iqn',
            node_id=self.node.id,
            connector_id='fake_iqn_initiator')
        obj_utils.create_test_volume_target(
            self.context, node_id=self.node.id, volume_type='iscsi',
            boot_index=0, volume_id='1234', uuid=vol_id,
            properties={'target_lun': 0,
                        'target_portal': 'fake_host:3260',
                        'target_iqn': 'fake_iqn',
                        'auth_username': 'fake_username',
                        'auth_password': 'fake_password'})
        obj_utils.create_test_volume_target(
            self.context, node_id=self.node.id, volume_type='iscsi',
            boot_index=1, volume_id='1235', uuid=vol_id2,
            properties={'target_lun': 1,
                        'target_portal': 'fake_host:3260',
                        'target_iqn': 'fake_iqn',
                        'auth_username': 'fake_username_1',
                        'auth_password': 'fake_password_1'})
        self.node.driver_internal_info.update({'boot_from_volume': vol_id})
        self._test_build_pxe_config_options_ipxe(boot_from_volume=True)

    def test__build_pxe_config_options_ipxe_and_iscsi_boot_from_lists(self):
        vol_id = uuidutils.generate_uuid()
        vol_id2 = uuidutils.generate_uuid()
        obj_utils.create_test_volume_connector(
            self.context,
            uuid=uuidutils.generate_uuid(),
            type='iqn',
            node_id=self.node.id,
            connector_id='fake_iqn_initiator')
        obj_utils.create_test_volume_target(
            self.context, node_id=self.node.id, volume_type='iscsi',
            boot_index=0, volume_id='1234', uuid=vol_id,
            properties={'target_luns': [0, 2],
                        'target_portals': ['fake_host:3260',
                                           'faker_host:3261'],
                        'target_iqns': ['fake_iqn', 'faker_iqn'],
                        'auth_username': 'fake_username',
                        'auth_password': 'fake_password'})
        obj_utils.create_test_volume_target(
            self.context, node_id=self.node.id, volume_type='iscsi',
            boot_index=1, volume_id='1235', uuid=vol_id2,
            properties={'target_lun': [1, 3],
                        'target_portal': ['fake_host:3260', 'faker_host:3261'],
                        'target_iqn': ['fake_iqn', 'faker_iqn'],
                        'auth_username': 'fake_username_1',
                        'auth_password': 'fake_password_1'})
        self.node.driver_internal_info.update({'boot_from_volume': vol_id})
        self._test_build_pxe_config_options_ipxe(boot_from_volume=True)

    def test__get_volume_pxe_options(self):
        vol_id = uuidutils.generate_uuid()
        vol_id2 = uuidutils.generate_uuid()
        obj_utils.create_test_volume_connector(
            self.context,
            uuid=uuidutils.generate_uuid(),
            type='iqn',
            node_id=self.node.id,
            connector_id='fake_iqn_initiator')
        obj_utils.create_test_volume_target(
            self.context, node_id=self.node.id, volume_type='iscsi',
            boot_index=0, volume_id='1234', uuid=vol_id,
            properties={'target_lun': [0, 1, 3],
                        'target_portal': 'fake_host:3260',
                        'target_iqns': 'fake_iqn',
                        'auth_username': 'fake_username',
                        'auth_password': 'fake_password'})
        obj_utils.create_test_volume_target(
            self.context, node_id=self.node.id, volume_type='iscsi',
            boot_index=1, volume_id='1235', uuid=vol_id2,
            properties={'target_lun': 1,
                        'target_portal': 'fake_host:3260',
                        'target_iqn': 'fake_iqn',
                        'auth_username': 'fake_username_1',
                        'auth_password': 'fake_password_1'})
        self.node.driver_internal_info.update({'boot_from_volume': vol_id})
        driver_internal_info = self.node.driver_internal_info
        driver_internal_info['boot_from_volume'] = vol_id
        self.node.driver_internal_info = driver_internal_info
        self.node.save()

        expected = {'boot_from_volume': True,
                    'username': 'fake_username', 'password': 'fake_password',
                    'iscsi_boot_url': 'iscsi:fake_host::3260:0:fake_iqn',
                    'iscsi_initiator_iqn': 'fake_iqn_initiator',
                    'iscsi_volumes': [{
                        'url': 'iscsi:fake_host::3260:1:fake_iqn',
                        'username': 'fake_username_1',
                        'password': 'fake_password_1'
                    }]
                    }
        with task_manager.acquire(self.context, self.node.uuid,
                                  shared=True) as task:
            options = pxe._get_volume_pxe_options(task)
        self.assertEqual(expected, options)

    def test__get_volume_pxe_options_unsupported_volume_type(self):
        vol_id = uuidutils.generate_uuid()
        obj_utils.create_test_volume_target(
            self.context, node_id=self.node.id, volume_type='fake_type',
            boot_index=0, volume_id='1234', uuid=vol_id,
            properties={'foo': 'bar'})

        driver_internal_info = self.node.driver_internal_info
        driver_internal_info['boot_from_volume'] = vol_id
        self.node.driver_internal_info = driver_internal_info
        self.node.save()
        with task_manager.acquire(self.context, self.node.uuid,
                                  shared=True) as task:
            options = pxe._get_volume_pxe_options(task)
        self.assertEqual({}, options)

    def test__get_volume_pxe_options_unsupported_additional_volume_type(self):
        vol_id = uuidutils.generate_uuid()
        vol_id2 = uuidutils.generate_uuid()
        obj_utils.create_test_volume_target(
            self.context, node_id=self.node.id, volume_type='iscsi',
            boot_index=0, volume_id='1234', uuid=vol_id,
            properties={'target_lun': 0,
                        'target_portal': 'fake_host:3260',
                        'target_iqn': 'fake_iqn',
                        'auth_username': 'fake_username',
                        'auth_password': 'fake_password'})
        obj_utils.create_test_volume_target(
            self.context, node_id=self.node.id, volume_type='fake_type',
            boot_index=1, volume_id='1234', uuid=vol_id2,
            properties={'foo': 'bar'})

        driver_internal_info = self.node.driver_internal_info
        driver_internal_info['boot_from_volume'] = vol_id
        self.node.driver_internal_info = driver_internal_info
        self.node.save()
        with task_manager.acquire(self.context, self.node.uuid,
                                  shared=True) as task:
            options = pxe._get_volume_pxe_options(task)
        self.assertEqual([], options['iscsi_volumes'])

    def test__build_pxe_config_options_ipxe_rescue(self):
        self._test_build_pxe_config_options_ipxe(mode='rescue')

    def test__build_pxe_config_options_ipxe_rescue_swift(self):
        self._test_build_pxe_config_options_ipxe(mode='rescue',
                                                 ipxe_use_swift=True)

    def test__build_pxe_config_options_ipxe_rescue_timeout(self):
        self._test_build_pxe_config_options_ipxe(mode='rescue',
                                                 ipxe_timeout=120)

    @mock.patch.object(deploy_utils, 'fetch_images', autospec=True)
    def test__cache_tftp_images_master_path(self, mock_fetch_image):
        temp_dir = tempfile.mkdtemp()
        self.config(tftp_root=temp_dir, group='pxe')
        self.config(tftp_master_path=os.path.join(temp_dir,
                                                  'tftp_master_path'),
                    group='pxe')
        image_path = os.path.join(temp_dir, self.node.uuid,
                                  'deploy_kernel')
        image_info = {'deploy_kernel': ('deploy_kernel', image_path)}
        fileutils.ensure_tree(CONF.pxe.tftp_master_path)

        pxe._cache_ramdisk_kernel(None, self.node, image_info)

        mock_fetch_image.assert_called_once_with(None,
                                                 mock.ANY,
                                                 [('deploy_kernel',
                                                   image_path)],
                                                 True)

    @mock.patch.object(pxe, 'TFTPImageCache', lambda: None)
    @mock.patch.object(fileutils, 'ensure_tree', autospec=True)
    @mock.patch.object(deploy_utils, 'fetch_images', autospec=True)
    def test__cache_ramdisk_kernel(self, mock_fetch_image, mock_ensure_tree):
        self.config(ipxe_enabled=False, group='pxe')
        fake_pxe_info = {'foo': 'bar'}
        expected_path = os.path.join(CONF.pxe.tftp_root, self.node.uuid)

        pxe._cache_ramdisk_kernel(self.context, self.node, fake_pxe_info)
        mock_ensure_tree.assert_called_with(expected_path)
        mock_fetch_image.assert_called_once_with(
            self.context, mock.ANY, list(fake_pxe_info.values()), True)

    @mock.patch.object(pxe, 'TFTPImageCache', lambda: None)
    @mock.patch.object(fileutils, 'ensure_tree', autospec=True)
    @mock.patch.object(deploy_utils, 'fetch_images', autospec=True)
    def test__cache_ramdisk_kernel_ipxe(self, mock_fetch_image,
                                        mock_ensure_tree):
        self.config(ipxe_enabled=True, group='pxe')
        fake_pxe_info = {'foo': 'bar'}
        expected_path = os.path.join(CONF.deploy.http_root,
                                     self.node.uuid)

        pxe._cache_ramdisk_kernel(self.context, self.node, fake_pxe_info)
        mock_ensure_tree.assert_called_with(expected_path)
        mock_fetch_image.assert_called_once_with(self.context, mock.ANY,
                                                 list(fake_pxe_info.values()),
                                                 True)

    @mock.patch.object(pxe.LOG, 'error', autospec=True)
    def test_validate_boot_parameters_for_trusted_boot_one(self, mock_log):
        properties = {'capabilities': 'boot_mode:uefi'}
        instance_info = {"boot_option": "netboot"}
        self.node.properties = properties
        self.node.instance_info['capabilities'] = instance_info
        self.node.driver_internal_info['is_whole_disk_image'] = False
        self.assertRaises(exception.InvalidParameterValue,
                          pxe.validate_boot_parameters_for_trusted_boot,
                          self.node)
        self.assertTrue(mock_log.called)

    @mock.patch.object(pxe.LOG, 'error', autospec=True)
    def test_validate_boot_parameters_for_trusted_boot_two(self, mock_log):
        properties = {'capabilities': 'boot_mode:bios'}
        instance_info = {"boot_option": "local"}
        self.node.properties = properties
        self.node.instance_info['capabilities'] = instance_info
        self.node.driver_internal_info['is_whole_disk_image'] = False
        self.assertRaises(exception.InvalidParameterValue,
                          pxe.validate_boot_parameters_for_trusted_boot,
                          self.node)
        self.assertTrue(mock_log.called)

    @mock.patch.object(pxe.LOG, 'error', autospec=True)
    def test_validate_boot_parameters_for_trusted_boot_three(self, mock_log):
        properties = {'capabilities': 'boot_mode:bios'}
        instance_info = {"boot_option": "netboot"}
        self.node.properties = properties
        self.node.instance_info['capabilities'] = instance_info
        self.node.driver_internal_info['is_whole_disk_image'] = True
        self.assertRaises(exception.InvalidParameterValue,
                          pxe.validate_boot_parameters_for_trusted_boot,
                          self.node)
        self.assertTrue(mock_log.called)

    @mock.patch.object(pxe.LOG, 'error', autospec=True)
    def test_validate_boot_parameters_for_trusted_boot_pass(self, mock_log):
        properties = {'capabilities': 'boot_mode:bios'}
        instance_info = {"boot_option": "netboot"}
        self.node.properties = properties
        self.node.instance_info['capabilities'] = instance_info
        self.node.driver_internal_info['is_whole_disk_image'] = False
        pxe.validate_boot_parameters_for_trusted_boot(self.node)
        self.assertFalse(mock_log.called)


@mock.patch.object(ironic_utils, 'unlink_without_raise', autospec=True)
@mock.patch.object(pxe_utils, 'clean_up_pxe_config', autospec=True)
@mock.patch.object(pxe, 'TFTPImageCache', autospec=True)
class CleanUpPxeEnvTestCase(db_base.DbTestCase):
    def setUp(self):
        super(CleanUpPxeEnvTestCase, self).setUp()
        instance_info = INST_INFO_DICT
        instance_info['deploy_key'] = 'fake-56789'
        self.node = obj_utils.create_test_node(
            self.context, boot_interface='pxe',
            instance_info=instance_info,
            driver_info=DRV_INFO_DICT,
            driver_internal_info=DRV_INTERNAL_INFO_DICT,
        )

    def test__clean_up_pxe_env(self, mock_cache, mock_pxe_clean,
                               mock_unlink):
        image_info = {'label': ['', 'deploy_kernel']}
        with task_manager.acquire(self.context, self.node.uuid,
                                  shared=True) as task:
            pxe._clean_up_pxe_env(task, image_info)
            mock_pxe_clean.assert_called_once_with(task)
            mock_unlink.assert_any_call('deploy_kernel')
        mock_cache.return_value.clean_up.assert_called_once_with()


@mock.patch.object(pxe.PXEBoot, '__init__', lambda self: None)
class PXEBootTestCase(db_base.DbTestCase):

    driver = 'fake-hardware'
    boot_interface = 'pxe'
    driver_info = DRV_INFO_DICT
    driver_internal_info = DRV_INTERNAL_INFO_DICT

    def setUp(self):
        super(PXEBootTestCase, self).setUp()
        self.context.auth_token = 'fake'
        self.config_temp_dir('tftp_root', group='pxe')
        self.config_temp_dir('images_path', group='pxe')
        self.config_temp_dir('http_root', group='deploy')
        instance_info = INST_INFO_DICT
        instance_info['deploy_key'] = 'fake-56789'

        self.config(enabled_boot_interfaces=[self.boot_interface, 'fake'])
        self.node = obj_utils.create_test_node(
            self.context,
            driver=self.driver,
            boot_interface=self.boot_interface,
            # Avoid fake properties in get_properties() output
            vendor_interface='no-vendor',
            instance_info=instance_info,
            driver_info=self.driver_info,
            driver_internal_info=self.driver_internal_info)
        self.port = obj_utils.create_test_port(self.context,
                                               node_id=self.node.id)
        self.config(group='conductor', api_url='http://127.0.0.1:1234/')

    def test_get_properties(self):
        expected = pxe.COMMON_PROPERTIES
        expected.update(agent_base_vendor.VENDOR_PROPERTIES)
        with task_manager.acquire(self.context, self.node.uuid,
                                  shared=True) as task:
            self.assertEqual(expected, task.driver.get_properties())

    @mock.patch.object(base_image_service.BaseImageService, '_show',
                       autospec=True)
    def test_validate_good(self, mock_glance):
        mock_glance.return_value = {'properties': {'kernel_id': 'fake-kernel',
                                                   'ramdisk_id': 'fake-initr'}}
        with task_manager.acquire(self.context, self.node.uuid,
                                  shared=True) as task:
            task.driver.boot.validate(task)

    @mock.patch.object(base_image_service.BaseImageService, '_show',
                       autospec=True)
    def test_validate_good_whole_disk_image(self, mock_glance):
        with task_manager.acquire(self.context, self.node.uuid,
                                  shared=True) as task:
            task.node.driver_internal_info['is_whole_disk_image'] = True
            task.driver.boot.validate(task)

    @mock.patch.object(base_image_service.BaseImageService, '_show',
                       autospec=True)
    @mock.patch.object(noop_storage.NoopStorage, 'should_write_image',
                       autospec=True)
    def test_validate_skip_check_write_image_false(self, mock_write,
                                                   mock_glance):
        mock_write.return_value = False
        with task_manager.acquire(self.context, self.node.uuid,
                                  shared=True) as task:
            task.driver.boot.validate(task)
        self.assertFalse(mock_glance.called)

    def test_validate_fail_missing_deploy_kernel(self):
        with task_manager.acquire(self.context, self.node.uuid,
                                  shared=True) as task:
            del task.node.driver_info['deploy_kernel']
            self.assertRaises(exception.MissingParameterValue,
                              task.driver.boot.validate, task)

    def test_validate_fail_missing_deploy_ramdisk(self):
        with task_manager.acquire(self.context, self.node.uuid,
                                  shared=True) as task:
            del task.node.driver_info['deploy_ramdisk']
            self.assertRaises(exception.MissingParameterValue,
                              task.driver.boot.validate, task)

    def test_validate_fail_missing_image_source(self):
        info = dict(INST_INFO_DICT)
        del info['image_source']
        self.node.instance_info = json.dumps(info)
        with task_manager.acquire(self.context, self.node.uuid,
                                  shared=True) as task:
            task.node['instance_info'] = json.dumps(info)
            self.assertRaises(exception.MissingParameterValue,
                              task.driver.boot.validate, task)

    def test_validate_fail_no_port(self):
        new_node = obj_utils.create_test_node(
            self.context,
            uuid='aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee',
            driver=self.driver, boot_interface=self.boot_interface,
            instance_info=INST_INFO_DICT, driver_info=DRV_INFO_DICT)
        with task_manager.acquire(self.context, new_node.uuid,
                                  shared=True) as task:
            self.assertRaises(exception.MissingParameterValue,
                              task.driver.boot.validate, task)

    def test_validate_fail_trusted_boot_with_secure_boot(self):
        instance_info = {"boot_option": "netboot",
                         "secure_boot": "true",
                         "trusted_boot": "true"}
        properties = {'capabilities': 'trusted_boot:true'}
        with task_manager.acquire(self.context, self.node.uuid,
                                  shared=True) as task:
            task.node.instance_info['capabilities'] = instance_info
            task.node.properties = properties
            task.node.driver_internal_info['is_whole_disk_image'] = False
            self.assertRaises(exception.InvalidParameterValue,
                              task.driver.boot.validate, task)

    def test_validate_fail_invalid_trusted_boot_value(self):
        properties = {'capabilities': 'trusted_boot:value'}
        instance_info = {"trusted_boot": "value"}
        with task_manager.acquire(self.context, self.node.uuid,
                                  shared=True) as task:
            task.node.properties = properties
            task.node.instance_info['capabilities'] = instance_info
            self.assertRaises(exception.InvalidParameterValue,
                              task.driver.boot.validate, task)

    @mock.patch.object(base_image_service.BaseImageService, '_show',
                       autospec=True)
    def test_validate_fail_no_image_kernel_ramdisk_props(self, mock_glance):
        mock_glance.return_value = {'properties': {}}
        with task_manager.acquire(self.context, self.node.uuid,
                                  shared=True) as task:
            self.assertRaises(exception.MissingParameterValue,
                              task.driver.boot.validate,
                              task)

    @mock.patch.object(base_image_service.BaseImageService, '_show',
                       autospec=True)
    def test_validate_fail_glance_image_doesnt_exists(self, mock_glance):
        mock_glance.side_effect = exception.ImageNotFound('not found')
        with task_manager.acquire(self.context, self.node.uuid,
                                  shared=True) as task:
            self.assertRaises(exception.InvalidParameterValue,
                              task.driver.boot.validate, task)

    @mock.patch.object(base_image_service.BaseImageService, '_show',
                       autospec=True)
    def test_validate_fail_glance_conn_problem(self, mock_glance):
        exceptions = (exception.GlanceConnectionFailed('connection fail'),
                      exception.ImageNotAuthorized('not authorized'),
                      exception.Invalid('invalid'))
        mock_glance.side_effect = exceptions
        for exc in exceptions:
            with task_manager.acquire(self.context, self.node.uuid,
                                      shared=True) as task:
                self.assertRaises(exception.InvalidParameterValue,
                                  task.driver.boot.validate, task)

    @mock.patch.object(manager_utils, 'node_get_boot_mode', autospec=True)
    @mock.patch.object(manager_utils, 'node_set_boot_device', autospec=True)
    @mock.patch.object(dhcp_factory, 'DHCPFactory')
    @mock.patch.object(pxe, '_get_instance_image_info', autospec=True)
    @mock.patch.object(pxe, '_get_image_info', autospec=True)
    @mock.patch.object(pxe, '_cache_ramdisk_kernel', autospec=True)
    @mock.patch.object(pxe, '_build_pxe_config_options', autospec=True)
    @mock.patch.object(pxe_utils, 'create_pxe_config', autospec=True)
    def _test_prepare_ramdisk(self, mock_pxe_config,
                              mock_build_pxe, mock_cache_r_k,
                              mock_deploy_img_info,
                              mock_instance_img_info,
                              dhcp_factory_mock,
                              set_boot_device_mock,
                              get_boot_mode_mock,
                              uefi=False,
                              cleaning=False,
                              ipxe_use_swift=False,
                              whole_disk_image=False,
                              mode='deploy',
                              node_boot_mode=None):
        mock_build_pxe.return_value = {}
        kernel_label = '%s_kernel' % mode
        ramdisk_label = '%s_ramdisk' % mode
        mock_deploy_img_info.return_value = {kernel_label: 'a',
                                             ramdisk_label: 'r'}
        if whole_disk_image:
            mock_instance_img_info.return_value = {}
        else:
            mock_instance_img_info.return_value = {'kernel': 'b'}
        mock_pxe_config.return_value = None
        mock_cache_r_k.return_value = None
        provider_mock = mock.MagicMock()
        dhcp_factory_mock.return_value = provider_mock
        get_boot_mode_mock.return_value = node_boot_mode
        driver_internal_info = self.node.driver_internal_info
        driver_internal_info['is_whole_disk_image'] = whole_disk_image
        self.node.driver_internal_info = driver_internal_info
        if mode == 'rescue':
            mock_deploy_img_info.return_value = {
                'rescue_kernel': 'a',
                'rescue_ramdisk': 'r'}
        self.node.save()
        with task_manager.acquire(self.context, self.node.uuid) as task:
            dhcp_opts = pxe_utils.dhcp_options_for_instance(task)
            task.driver.boot.prepare_ramdisk(task, {'foo': 'bar'})
            mock_deploy_img_info.assert_called_once_with(task.node, mode=mode)
            provider_mock.update_dhcp.assert_called_once_with(task, dhcp_opts)
            if self.node.provision_state == states.DEPLOYING:
                get_boot_mode_mock.assert_called_once_with(task)
            set_boot_device_mock.assert_called_once_with(task,
                                                         boot_devices.PXE,
                                                         persistent=False)
            if ipxe_use_swift:
                if whole_disk_image:
                    self.assertFalse(mock_cache_r_k.called)
                else:
                    mock_cache_r_k.assert_called_once_with(
                        self.context, task.node,
                        {'kernel': 'b'})
                mock_instance_img_info.assert_called_once_with(task.node,
                                                               self.context)
            elif not cleaning and mode == 'deploy':
                mock_cache_r_k.assert_called_once_with(
                    self.context, task.node,
                    {'deploy_kernel': 'a', 'deploy_ramdisk': 'r',
                     'kernel': 'b'})
                mock_instance_img_info.assert_called_once_with(task.node,
                                                               self.context)
            elif mode == 'deploy':
                    mock_cache_r_k.assert_called_once_with(
                        self.context, task.node,
                        {'deploy_kernel': 'a', 'deploy_ramdisk': 'r'})
            elif mode == 'rescue':
                    mock_cache_r_k.assert_called_once_with(
                        self.context, task.node,
                        {'rescue_kernel': 'a', 'rescue_ramdisk': 'r'})
            if uefi:
                mock_pxe_config.assert_called_once_with(
                    task, {'foo': 'bar'}, CONF.pxe.uefi_pxe_config_template)
            else:
                mock_pxe_config.assert_called_once_with(
                    task, {'foo': 'bar'}, CONF.pxe.pxe_config_template)

    def test_prepare_ramdisk(self):
        self.node.provision_state = states.DEPLOYING
        self.node.save()
        self._test_prepare_ramdisk()

    def test_prepare_ramdisk_rescue(self):
        self.node.provision_state = states.RESCUING
        self.node.save()
        self._test_prepare_ramdisk(mode='rescue')

    def test_prepare_ramdisk_uefi(self):
        self.node.provision_state = states.DEPLOYING
        self.node.save()
        properties = self.node.properties
        properties['capabilities'] = 'boot_mode:uefi'
        self.node.properties = properties
        self.node.save()
        self._test_prepare_ramdisk(uefi=True)

    @mock.patch.object(os.path, 'isfile', lambda path: True)
    @mock.patch.object(common_utils, 'file_has_content', lambda *args: False)
    @mock.patch('ironic.common.utils.write_to_file', autospec=True)
    @mock.patch('ironic.common.utils.render_template', autospec=True)
    def test_prepare_ramdisk_ipxe_with_copy_file_different(
            self, render_mock, write_mock):
        self.node.provision_state = states.DEPLOYING
        self.node.save()
        self.config(group='pxe', ipxe_enabled=True)
        self.config(group='deploy', http_url='http://myserver')
        render_mock.return_value = 'foo'
        self._test_prepare_ramdisk()
        write_mock.assert_called_once_with(
            os.path.join(
                CONF.deploy.http_root,
                os.path.basename(CONF.pxe.ipxe_boot_script)),
            'foo')
        render_mock.assert_called_once_with(
            CONF.pxe.ipxe_boot_script,
            {'ipxe_for_mac_uri': 'pxelinux.cfg/'})

    @mock.patch.object(os.path, 'isfile', lambda path: False)
    @mock.patch('ironic.common.utils.file_has_content', autospec=True)
    @mock.patch('ironic.common.utils.write_to_file', autospec=True)
    @mock.patch('ironic.common.utils.render_template', autospec=True)
    def test_prepare_ramdisk_ipxe_with_copy_no_file(
            self, render_mock, write_mock, file_has_content_mock):
        self.node.provision_state = states.DEPLOYING
        self.node.save()
        self.config(group='pxe', ipxe_enabled=True)
        self.config(group='deploy', http_url='http://myserver')
        render_mock.return_value = 'foo'
        self._test_prepare_ramdisk()
        self.assertFalse(file_has_content_mock.called)
        write_mock.assert_called_once_with(
            os.path.join(
                CONF.deploy.http_root,
                os.path.basename(CONF.pxe.ipxe_boot_script)),
            'foo')
        render_mock.assert_called_once_with(
            CONF.pxe.ipxe_boot_script,
            {'ipxe_for_mac_uri': 'pxelinux.cfg/'})

    @mock.patch.object(os.path, 'isfile', lambda path: True)
    @mock.patch.object(common_utils, 'file_has_content', lambda *args: True)
    @mock.patch('ironic.common.utils.write_to_file', autospec=True)
    @mock.patch('ironic.common.utils.render_template', autospec=True)
    def test_prepare_ramdisk_ipxe_without_copy(
            self, render_mock, write_mock):
        self.node.provision_state = states.DEPLOYING
        self.node.save()
        self.config(group='pxe', ipxe_enabled=True)
        self.config(group='deploy', http_url='http://myserver')
        self._test_prepare_ramdisk()
        self.assertFalse(write_mock.called)

    @mock.patch.object(common_utils, 'render_template', lambda *args: 'foo')
    @mock.patch('ironic.common.utils.write_to_file', autospec=True)
    def test_prepare_ramdisk_ipxe_swift(self, write_mock):
        self.node.provision_state = states.DEPLOYING
        self.node.save()
        self.config(group='pxe', ipxe_enabled=True)
        self.config(group='pxe', ipxe_use_swift=True)
        self.config(group='deploy', http_url='http://myserver')
        self._test_prepare_ramdisk(ipxe_use_swift=True)
        write_mock.assert_called_once_with(
            os.path.join(
                CONF.deploy.http_root,
                os.path.basename(CONF.pxe.ipxe_boot_script)),
            'foo')

    @mock.patch.object(common_utils, 'render_template', lambda *args: 'foo')
    @mock.patch('ironic.common.utils.write_to_file', autospec=True)
    def test_prepare_ramdisk_ipxe_swift_whole_disk_image(
            self, write_mock):
        self.node.provision_state = states.DEPLOYING
        self.node.save()
        self.config(group='pxe', ipxe_enabled=True)
        self.config(group='pxe', ipxe_use_swift=True)
        self.config(group='deploy', http_url='http://myserver')
        self._test_prepare_ramdisk(ipxe_use_swift=True, whole_disk_image=True)
        write_mock.assert_called_once_with(
            os.path.join(
                CONF.deploy.http_root,
                os.path.basename(CONF.pxe.ipxe_boot_script)),
            'foo')

    def test_prepare_ramdisk_cleaning(self):
        self.node.provision_state = states.CLEANING
        self.node.save()
        self._test_prepare_ramdisk(cleaning=True)

    @mock.patch.object(manager_utils, 'node_set_boot_mode', autospec=True)
    def test_prepare_ramdisk_set_boot_mode_on_bm(
            self, set_boot_mode_mock):
        self.node.provision_state = states.DEPLOYING
        properties = self.node.properties
        properties['capabilities'] = 'boot_mode:uefi'
        self.node.properties = properties
        self.node.save()
        self._test_prepare_ramdisk(uefi=True)
        set_boot_mode_mock.assert_called_once_with(mock.ANY, boot_modes.UEFI)

    @mock.patch.object(manager_utils, 'node_set_boot_mode', autospec=True)
    def test_prepare_ramdisk_set_boot_mode_on_ironic(
            self, set_boot_mode_mock):
        self.node.provision_state = states.DEPLOYING
        self.node.save()
        self._test_prepare_ramdisk(node_boot_mode=boot_modes.LEGACY_BIOS)

        with task_manager.acquire(self.context, self.node.uuid) as task:
            driver_internal_info = task.node.driver_internal_info
            self.assertIn('deploy_boot_mode', driver_internal_info)
            self.assertEqual(boot_modes.LEGACY_BIOS,
                             driver_internal_info['deploy_boot_mode'])
            self.assertEqual(set_boot_mode_mock.call_count, 0)

    @mock.patch.object(manager_utils, 'node_set_boot_mode', autospec=True)
    def test_prepare_ramdisk_set_default_boot_mode_on_ironic_bios(
            self, set_boot_mode_mock):
        self.node.provision_state = states.DEPLOYING
        self.node.save()

        self.config(default_boot_mode=boot_modes.LEGACY_BIOS, group='deploy')

        self._test_prepare_ramdisk()

        with task_manager.acquire(self.context, self.node.uuid) as task:
            driver_internal_info = task.node.driver_internal_info
            self.assertIn('deploy_boot_mode', driver_internal_info)
            self.assertEqual(boot_modes.LEGACY_BIOS,
                             driver_internal_info['deploy_boot_mode'])
            self.assertEqual(set_boot_mode_mock.call_count, 1)

    @mock.patch.object(manager_utils, 'node_set_boot_mode', autospec=True)
    def test_prepare_ramdisk_set_default_boot_mode_on_ironic_uefi(
            self, set_boot_mode_mock):
        self.node.provision_state = states.DEPLOYING
        self.node.save()

        self.config(default_boot_mode=boot_modes.UEFI, group='deploy')

        self._test_prepare_ramdisk(uefi=True)

        with task_manager.acquire(self.context, self.node.uuid) as task:
            driver_internal_info = task.node.driver_internal_info
            self.assertIn('deploy_boot_mode', driver_internal_info)
            self.assertEqual(boot_modes.UEFI,
                             driver_internal_info['deploy_boot_mode'])
            self.assertEqual(set_boot_mode_mock.call_count, 1)

    @mock.patch.object(manager_utils, 'node_set_boot_mode', autospec=True)
    def test_prepare_ramdisk_conflicting_boot_modes(
            self, set_boot_mode_mock):
        self.node.provision_state = states.DEPLOYING
        properties = self.node.properties
        properties['capabilities'] = 'boot_mode:uefi'
        self.node.properties = properties
        self.node.save()
        self._test_prepare_ramdisk(uefi=True,
                                   node_boot_mode=boot_modes.LEGACY_BIOS)
        set_boot_mode_mock.assert_called_once_with(mock.ANY, boot_modes.UEFI)

    @mock.patch.object(manager_utils, 'node_set_boot_mode', autospec=True)
    def test_prepare_ramdisk_conflicting_boot_modes_set_unsupported(
            self, set_boot_mode_mock):
        self.node.provision_state = states.DEPLOYING
        properties = self.node.properties
        properties['capabilities'] = 'boot_mode:uefi'
        self.node.properties = properties
        self.node.save()
        set_boot_mode_mock.side_effect = exception.UnsupportedDriverExtension(
            extension='management', driver='test-driver'
        )
        self.assertRaises(exception.UnsupportedDriverExtension,
                          self._test_prepare_ramdisk,
                          uefi=True, node_boot_mode=boot_modes.LEGACY_BIOS)

    @mock.patch.object(manager_utils, 'node_set_boot_mode', autospec=True)
    def test_prepare_ramdisk_set_boot_mode_not_called(
            self, set_boot_mode_mock):
        self.node.provision_state = states.DEPLOYING
        self.node.save()
        properties = self.node.properties
        properties['capabilities'] = 'boot_mode:uefi'
        self.node.properties = properties
        self.node.save()
        self._test_prepare_ramdisk(uefi=True, node_boot_mode=boot_modes.UEFI)
        self.assertEqual(set_boot_mode_mock.call_count, 0)

    @mock.patch.object(pxe, '_clean_up_pxe_env', autospec=True)
    @mock.patch.object(pxe, '_get_image_info', autospec=True)
    def _test_clean_up_ramdisk(self, get_image_info_mock,
                               clean_up_pxe_env_mock, mode='deploy'):
        with task_manager.acquire(self.context, self.node.uuid) as task:
            kernel_label = '%s_kernel' % mode
            ramdisk_label = '%s_ramdisk' % mode
            image_info = {kernel_label: ['', '/path/to/' + kernel_label],
                          ramdisk_label: ['', '/path/to/' + ramdisk_label]}
            get_image_info_mock.return_value = image_info
            task.driver.boot.clean_up_ramdisk(task)
            clean_up_pxe_env_mock.assert_called_once_with(task, image_info)
            get_image_info_mock.assert_called_once_with(task.node, mode=mode)

    def test_clean_up_ramdisk(self):
        self.node.provision_state = states.DEPLOYING
        self.node.save()
        self._test_clean_up_ramdisk()

    def test_clean_up_ramdisk_rescue(self):
        self.node.provision_state = states.RESCUING
        self.node.save()
        self._test_clean_up_ramdisk(mode='rescue')

    @mock.patch.object(manager_utils, 'node_set_boot_device', autospec=True)
    @mock.patch.object(deploy_utils, 'switch_pxe_config', autospec=True)
    @mock.patch.object(dhcp_factory, 'DHCPFactory', autospec=True)
    @mock.patch.object(pxe, '_cache_ramdisk_kernel', autospec=True)
    @mock.patch.object(pxe, '_get_instance_image_info', autospec=True)
    def test_prepare_instance_netboot(
            self, get_image_info_mock, cache_mock,
            dhcp_factory_mock, switch_pxe_config_mock,
            set_boot_device_mock):
        provider_mock = mock.MagicMock()
        dhcp_factory_mock.return_value = provider_mock
        image_info = {'kernel': ('', '/path/to/kernel'),
                      'ramdisk': ('', '/path/to/ramdisk')}
        get_image_info_mock.return_value = image_info
        with task_manager.acquire(self.context, self.node.uuid) as task:
            dhcp_opts = pxe_utils.dhcp_options_for_instance(task)
            pxe_config_path = pxe_utils.get_pxe_config_file_path(
                task.node.uuid)
            task.node.properties['capabilities'] = 'boot_mode:bios'
            task.node.driver_internal_info['root_uuid_or_disk_id'] = (
                "30212642-09d3-467f-8e09-21685826ab50")
            task.node.driver_internal_info['is_whole_disk_image'] = False

            task.driver.boot.prepare_instance(task)

            get_image_info_mock.assert_called_once_with(
                task.node, task.context)
            cache_mock.assert_called_once_with(
                task.context, task.node, image_info)
            provider_mock.update_dhcp.assert_called_once_with(task, dhcp_opts)
            switch_pxe_config_mock.assert_called_once_with(
                pxe_config_path, "30212642-09d3-467f-8e09-21685826ab50",
                'bios', False, False, False, False)
            set_boot_device_mock.assert_called_once_with(task,
                                                         boot_devices.PXE,
                                                         persistent=True)

    @mock.patch('os.path.isfile', return_value=False)
    @mock.patch.object(pxe_utils, 'create_pxe_config', autospec=True)
    @mock.patch.object(manager_utils, 'node_set_boot_device', autospec=True)
    @mock.patch.object(deploy_utils, 'switch_pxe_config', autospec=True)
    @mock.patch.object(dhcp_factory, 'DHCPFactory', autospec=True)
    @mock.patch.object(pxe, '_cache_ramdisk_kernel', autospec=True)
    @mock.patch.object(pxe, '_get_instance_image_info', autospec=True)
    def test_prepare_instance_netboot_active(
            self, get_image_info_mock, cache_mock,
            dhcp_factory_mock, switch_pxe_config_mock,
            set_boot_device_mock, create_pxe_config_mock, isfile_mock):
        provider_mock = mock.MagicMock()
        dhcp_factory_mock.return_value = provider_mock
        image_info = {'kernel': ('', '/path/to/kernel'),
                      'ramdisk': ('', '/path/to/ramdisk')}
        get_image_info_mock.return_value = image_info
        self.node.provision_state = states.ACTIVE
        self.node.save()
        with task_manager.acquire(self.context, self.node.uuid) as task:
            dhcp_opts = pxe_utils.dhcp_options_for_instance(task)
            pxe_config_path = pxe_utils.get_pxe_config_file_path(
                task.node.uuid)
            task.node.properties['capabilities'] = 'boot_mode:bios'
            task.node.driver_internal_info['root_uuid_or_disk_id'] = (
                "30212642-09d3-467f-8e09-21685826ab50")
            task.node.driver_internal_info['is_whole_disk_image'] = False

            task.driver.boot.prepare_instance(task)

            get_image_info_mock.assert_called_once_with(
                task.node, task.context)
            cache_mock.assert_called_once_with(
                task.context, task.node, image_info)
            provider_mock.update_dhcp.assert_called_once_with(task, dhcp_opts)
            create_pxe_config_mock.assert_called_once_with(
                task, mock.ANY, CONF.pxe.pxe_config_template)
            switch_pxe_config_mock.assert_called_once_with(
                pxe_config_path, "30212642-09d3-467f-8e09-21685826ab50",
                'bios', False, False, False, False)
            self.assertFalse(set_boot_device_mock.called)

    @mock.patch.object(manager_utils, 'node_set_boot_device', autospec=True)
    @mock.patch.object(deploy_utils, 'switch_pxe_config', autospec=True)
    @mock.patch.object(dhcp_factory, 'DHCPFactory')
    @mock.patch.object(pxe, '_cache_ramdisk_kernel', autospec=True)
    @mock.patch.object(pxe, '_get_instance_image_info', autospec=True)
    def test_prepare_instance_netboot_missing_root_uuid(
            self, get_image_info_mock, cache_mock,
            dhcp_factory_mock, switch_pxe_config_mock,
            set_boot_device_mock):
        provider_mock = mock.MagicMock()
        dhcp_factory_mock.return_value = provider_mock
        image_info = {'kernel': ('', '/path/to/kernel'),
                      'ramdisk': ('', '/path/to/ramdisk')}
        get_image_info_mock.return_value = image_info
        with task_manager.acquire(self.context, self.node.uuid) as task:
            dhcp_opts = pxe_utils.dhcp_options_for_instance(task)
            task.node.properties['capabilities'] = 'boot_mode:bios'
            task.node.driver_internal_info['is_whole_disk_image'] = False

            task.driver.boot.prepare_instance(task)

            get_image_info_mock.assert_called_once_with(
                task.node, task.context)
            cache_mock.assert_called_once_with(
                task.context, task.node, image_info)
            provider_mock.update_dhcp.assert_called_once_with(task, dhcp_opts)
            self.assertFalse(switch_pxe_config_mock.called)
            self.assertFalse(set_boot_device_mock.called)

    @mock.patch.object(pxe.LOG, 'warning', autospec=True)
    @mock.patch.object(pxe_utils, 'clean_up_pxe_config', autospec=True)
    @mock.patch.object(manager_utils, 'node_set_boot_device', autospec=True)
    @mock.patch.object(dhcp_factory, 'DHCPFactory')
    @mock.patch.object(pxe, '_cache_ramdisk_kernel', autospec=True)
    @mock.patch.object(pxe, '_get_instance_image_info', autospec=True)
    def test_prepare_instance_whole_disk_image_missing_root_uuid(
            self, get_image_info_mock, cache_mock,
            dhcp_factory_mock, set_boot_device_mock,
            clean_up_pxe_mock, log_mock):
        provider_mock = mock.MagicMock()
        dhcp_factory_mock.return_value = provider_mock
        get_image_info_mock.return_value = {}
        with task_manager.acquire(self.context, self.node.uuid) as task:
            dhcp_opts = pxe_utils.dhcp_options_for_instance(task)
            task.node.properties['capabilities'] = 'boot_mode:bios'
            task.node.driver_internal_info['is_whole_disk_image'] = True
            task.driver.boot.prepare_instance(task)
            get_image_info_mock.assert_called_once_with(
                task.node, task.context)
            cache_mock.assert_called_once_with(
                task.context, task.node, {})
            provider_mock.update_dhcp.assert_called_once_with(task, dhcp_opts)
            self.assertTrue(log_mock.called)
            clean_up_pxe_mock.assert_called_once_with(task)
            set_boot_device_mock.assert_called_once_with(
                task, boot_devices.DISK, persistent=True)

    @mock.patch('os.path.isfile', lambda filename: False)
    @mock.patch.object(pxe_utils, 'create_pxe_config', autospec=True)
    @mock.patch.object(deploy_utils, 'is_iscsi_boot', lambda task: True)
    @mock.patch.object(noop_storage.NoopStorage, 'should_write_image',
                       lambda task: False)
    @mock.patch.object(manager_utils, 'node_set_boot_device', autospec=True)
    @mock.patch.object(deploy_utils, 'switch_pxe_config', autospec=True)
    @mock.patch.object(dhcp_factory, 'DHCPFactory', autospec=True)
    @mock.patch.object(pxe, '_cache_ramdisk_kernel', autospec=True)
    @mock.patch.object(pxe, '_get_instance_image_info', autospec=True)
    def test_prepare_instance_netboot_iscsi(
            self, get_image_info_mock, cache_mock,
            dhcp_factory_mock, switch_pxe_config_mock,
            set_boot_device_mock, create_pxe_config_mock):
        http_url = 'http://192.1.2.3:1234'
        self.config(ipxe_enabled=True, group='pxe')
        self.config(http_url=http_url, group='deploy')
        provider_mock = mock.MagicMock()
        dhcp_factory_mock.return_value = provider_mock
        vol_id = uuidutils.generate_uuid()
        obj_utils.create_test_volume_target(
            self.context, node_id=self.node.id, volume_type='iscsi',
            boot_index=0, volume_id='1234', uuid=vol_id,
            properties={'target_lun': 0,
                        'target_portal': 'fake_host:3260',
                        'target_iqn': 'fake_iqn',
                        'auth_username': 'fake_username',
                        'auth_password': 'fake_password'})
        with task_manager.acquire(self.context, self.node.uuid) as task:
            task.node.driver_internal_info = {
                'boot_from_volume': vol_id}
            dhcp_opts = pxe_utils.dhcp_options_for_instance(task)
            pxe_config_path = pxe_utils.get_pxe_config_file_path(
                task.node.uuid)
            task.node.properties['capabilities'] = 'boot_mode:bios'
            task.driver.boot.prepare_instance(task)
            self.assertFalse(get_image_info_mock.called)
            self.assertFalse(cache_mock.called)
            provider_mock.update_dhcp.assert_called_once_with(task, dhcp_opts)
            create_pxe_config_mock.assert_called_once_with(
                task, mock.ANY, CONF.pxe.pxe_config_template)
            switch_pxe_config_mock.assert_called_once_with(
                pxe_config_path, None, boot_modes.LEGACY_BIOS, False,
                iscsi_boot=True, ramdisk_boot=False)
            set_boot_device_mock.assert_called_once_with(task,
                                                         boot_devices.PXE,
                                                         persistent=True)

    @mock.patch.object(manager_utils, 'node_set_boot_device', autospec=True)
    @mock.patch.object(pxe_utils, 'clean_up_pxe_config', autospec=True)
    def test_prepare_instance_localboot(self, clean_up_pxe_config_mock,
                                        set_boot_device_mock):
        with task_manager.acquire(self.context, self.node.uuid) as task:
            instance_info = task.node.instance_info
            instance_info['capabilities'] = {'boot_option': 'local'}
            task.node.instance_info = instance_info
            task.node.save()
            task.driver.boot.prepare_instance(task)
            clean_up_pxe_config_mock.assert_called_once_with(task)
            set_boot_device_mock.assert_called_once_with(task,
                                                         boot_devices.DISK,
                                                         persistent=True)

    @mock.patch.object(manager_utils, 'node_set_boot_device', autospec=True)
    @mock.patch.object(pxe_utils, 'clean_up_pxe_config', autospec=True)
    def test_is_force_persistent_boot_device_enabled(
            self, clean_up_pxe_config_mock, set_boot_device_mock):
        with task_manager.acquire(self.context, self.node.uuid) as task:
            instance_info = task.node.instance_info
            instance_info['capabilities'] = {'boot_option': 'local'}
            task.node.instance_info = instance_info
            task.node.save()
            task.driver.boot.prepare_instance(task)
            clean_up_pxe_config_mock.assert_called_once_with(task)
            driver_info = task.node.driver_info
            driver_info['force_persistent _boot_device'] = True
            task.node.driver_info = driver_info
            set_boot_device_mock.assert_called_once_with(task,
                                                         boot_devices.DISK,
                                                         persistent=True)

    @mock.patch.object(manager_utils, 'node_set_boot_device', autospec=True)
    @mock.patch.object(pxe_utils, 'clean_up_pxe_config', autospec=True)
    def test_prepare_instance_localboot_active(self, clean_up_pxe_config_mock,
                                               set_boot_device_mock):
        self.node.provision_state = states.ACTIVE
        self.node.save()
        with task_manager.acquire(self.context, self.node.uuid) as task:
            instance_info = task.node.instance_info
            instance_info['capabilities'] = {'boot_option': 'local'}
            task.node.instance_info = instance_info
            task.node.save()
            task.driver.boot.prepare_instance(task)
            clean_up_pxe_config_mock.assert_called_once_with(task)
            self.assertFalse(set_boot_device_mock.called)

    @mock.patch.object(manager_utils, 'node_set_boot_device', autospec=True)
    @mock.patch.object(deploy_utils, 'switch_pxe_config', autospec=True)
    @mock.patch.object(pxe_utils, 'create_pxe_config', autospec=True)
    @mock.patch.object(dhcp_factory, 'DHCPFactory', autospec=True)
    @mock.patch.object(pxe, '_cache_ramdisk_kernel', autospec=True)
    @mock.patch.object(pxe, '_get_instance_image_info', autospec=True)
    def _test_prepare_instance_ramdisk(
            self, get_image_info_mock, cache_mock,
            dhcp_factory_mock, create_pxe_config_mock,
            switch_pxe_config_mock,
            set_boot_device_mock, config_file_exits=False):
        image_info = {'kernel': ['', '/path/to/kernel'],
                      'ramdisk': ['', '/path/to/ramdisk']}
        get_image_info_mock.return_value = image_info
        provider_mock = mock.MagicMock()
        dhcp_factory_mock.return_value = provider_mock
        self.node.provision_state = states.DEPLOYING
        get_image_info_mock.return_value = image_info
        with task_manager.acquire(self.context, self.node.uuid) as task:
            instance_info = task.node.instance_info
            instance_info['capabilities'] = {'boot_option': 'ramdisk'}
            task.node.instance_info = instance_info
            task.node.save()
            dhcp_opts = pxe_utils.dhcp_options_for_instance(task)
            pxe_config_path = pxe_utils.get_pxe_config_file_path(
                task.node.uuid)
            task.driver.boot.prepare_instance(task)

            get_image_info_mock.assert_called_once_with(
                task.node, task.context)
            cache_mock.assert_called_once_with(
                task.context, task.node, image_info)
            provider_mock.update_dhcp.assert_called_once_with(task, dhcp_opts)
            if config_file_exits:
                self.assertFalse(create_pxe_config_mock.called)
            else:
                create_pxe_config_mock.assert_called_once_with(
                    task, mock.ANY, CONF.pxe.pxe_config_template)
            switch_pxe_config_mock.assert_called_once_with(
                pxe_config_path, None,
                'bios', False, iscsi_boot=False, ramdisk_boot=True)
            set_boot_device_mock.assert_called_once_with(task,
                                                         boot_devices.PXE,
                                                         persistent=True)

    @mock.patch.object(os.path, 'isfile', lambda path: True)
    def test_prepare_instance_ramdisk_pxe_conf_missing(self):
        self._test_prepare_instance_ramdisk(config_file_exits=True)

    @mock.patch.object(os.path, 'isfile', lambda path: False)
    def test_prepare_instance_ramdisk_pxe_conf_exists(self):
        self._test_prepare_instance_ramdisk(config_file_exits=False)

    @mock.patch.object(pxe, '_clean_up_pxe_env', autospec=True)
    @mock.patch.object(pxe, '_get_instance_image_info', autospec=True)
    def test_clean_up_instance(self, get_image_info_mock,
                               clean_up_pxe_env_mock):
        with task_manager.acquire(self.context, self.node.uuid) as task:
            image_info = {'kernel': ['', '/path/to/kernel'],
                          'ramdisk': ['', '/path/to/ramdisk']}
            get_image_info_mock.return_value = image_info
            task.driver.boot.clean_up_instance(task)
            clean_up_pxe_env_mock.assert_called_once_with(task, image_info)
            get_image_info_mock.assert_called_once_with(
                task.node, task.context)


class PXERamdiskDeployTestCase(db_base.DbTestCase):

    def setUp(self):
        super(PXERamdiskDeployTestCase, self).setUp()
        self.temp_dir = tempfile.mkdtemp()
        self.config(tftp_root=self.temp_dir, group='pxe')
        self.temp_dir = tempfile.mkdtemp()
        self.config(images_path=self.temp_dir, group='pxe')
        self.config(enabled_deploy_interfaces=['ramdisk'])
        self.config(enabled_boot_interfaces=['pxe'])
        for iface in drivers_base.ALL_INTERFACES:
            impl = 'fake'
            if iface == 'network':
                impl = 'noop'
            if iface == 'deploy':
                impl = 'ramdisk'
            if iface == 'boot':
                impl = 'pxe'
            config_kwarg = {'enabled_%s_interfaces' % iface: [impl],
                            'default_%s_interface' % iface: impl}
            self.config(**config_kwarg)
        self.config(enabled_hardware_types=['fake-hardware'])
        instance_info = INST_INFO_DICT
        self.node = obj_utils.create_test_node(
            self.context,
            driver='fake-hardware',
            instance_info=instance_info,
            driver_info=DRV_INFO_DICT,
            driver_internal_info=DRV_INTERNAL_INFO_DICT)
        self.port = obj_utils.create_test_port(self.context,
                                               node_id=self.node.id)

    @mock.patch.object(manager_utils, 'node_set_boot_device', autospec=True)
    @mock.patch.object(deploy_utils, 'switch_pxe_config', autospec=True)
    @mock.patch.object(dhcp_factory, 'DHCPFactory', autospec=True)
    @mock.patch.object(pxe, '_cache_ramdisk_kernel', autospec=True)
    @mock.patch.object(pxe, '_get_instance_image_info', autospec=True)
    def test_prepare_instance_ramdisk(
            self, get_image_info_mock, cache_mock,
            dhcp_factory_mock, switch_pxe_config_mock,
            set_boot_device_mock):
        provider_mock = mock.MagicMock()
        dhcp_factory_mock.return_value = provider_mock
        self.node.provision_state = states.DEPLOYING
        image_info = {'kernel': ('', '/path/to/kernel'),
                      'ramdisk': ('', '/path/to/ramdisk')}
        get_image_info_mock.return_value = image_info
        with task_manager.acquire(self.context, self.node.uuid) as task:
            dhcp_opts = pxe_utils.dhcp_options_for_instance(task)
            pxe_config_path = pxe_utils.get_pxe_config_file_path(
                task.node.uuid)
            task.node.properties['capabilities'] = 'boot_option:netboot'
            task.node.driver_internal_info['is_whole_disk_image'] = False
            task.driver.deploy.prepare(task)
            task.driver.deploy.deploy(task)

            get_image_info_mock.assert_called_once_with(
                task.node, task.context)
            cache_mock.assert_called_once_with(
                task.context, task.node, image_info)
            provider_mock.update_dhcp.assert_called_once_with(task, dhcp_opts)
            switch_pxe_config_mock.assert_called_once_with(
                pxe_config_path, None,
                'bios', False, iscsi_boot=False, ramdisk_boot=True)
            set_boot_device_mock.assert_called_once_with(task,
                                                         boot_devices.PXE,
                                                         persistent=True)

    @mock.patch.object(pxe.LOG, 'warning', autospec=True)
    @mock.patch.object(deploy_utils, 'switch_pxe_config', autospec=True)
    @mock.patch.object(dhcp_factory, 'DHCPFactory', autospec=True)
    @mock.patch.object(pxe, '_cache_ramdisk_kernel', autospec=True)
    @mock.patch.object(pxe, '_get_instance_image_info', autospec=True)
    def test_deploy(self, mock_image_info, mock_cache,
                    mock_dhcp_factory, mock_switch_config, mock_warning):
        image_info = {'kernel': ('', '/path/to/kernel'),
                      'ramdisk': ('', '/path/to/ramdisk')}
        mock_image_info.return_value = image_info
        i_info = self.node.instance_info
        i_info.update({'capabilities': {'boot_option': 'ramdisk'}})
        self.node.instance_info = i_info
        self.node.save()
        with task_manager.acquire(self.context, self.node.uuid) as task:
            self.assertIsNone(task.driver.deploy.deploy(task))
            mock_image_info.assert_called_once_with(
                task.node, task.context)
            mock_cache.assert_called_once_with(
                task.context, task.node, image_info)
            self.assertFalse(mock_warning.called)
        i_info['configdrive'] = 'meow'
        self.node.instance_info = i_info
        self.node.save()
        mock_warning.reset_mock()
        with task_manager.acquire(self.context, self.node.uuid) as task:
            self.assertIsNone(task.driver.deploy.deploy(task))
            self.assertTrue(mock_warning.called)

    @mock.patch.object(pxe.PXEBoot, 'prepare_instance', autospec=True)
    def test_prepare(self, mock_prepare_instance):
        node = self.node
        node.provision_state = states.DEPLOYING
        node.instance_info = {}
        node.save()
        with task_manager.acquire(self.context, node.uuid) as task:
            task.driver.deploy.prepare(task)
            self.assertFalse(mock_prepare_instance.called)
            self.assertEqual({'boot_option': 'ramdisk'},
                             task.node.instance_info['capabilities'])

    @mock.patch.object(pxe.PXEBoot, 'prepare_instance', autospec=True)
    def test_prepare_active(self, mock_prepare_instance):
        node = self.node
        node.provision_state = states.ACTIVE
        node.save()
        with task_manager.acquire(self.context, node.uuid) as task:
            task.driver.deploy.prepare(task)
            mock_prepare_instance.assert_called_once_with(mock.ANY, task)

    @mock.patch.object(pxe.PXEBoot, 'prepare_instance', autospec=True)
    def test_prepare_unrescuing(self, mock_prepare_instance):
        node = self.node
        node.provision_state = states.UNRESCUING
        node.save()
        with task_manager.acquire(self.context, node.uuid) as task:
            task.driver.deploy.prepare(task)
            mock_prepare_instance.assert_called_once_with(mock.ANY, task)

    @mock.patch.object(pxe.LOG, 'warning', autospec=True)
    @mock.patch.object(pxe.PXEBoot, 'prepare_instance', autospec=True)
    def test_prepare_fixes_and_logs_boot_option_warning(
            self, mock_prepare_instance, mock_warning):
        node = self.node
        node.properties['capabilities'] = 'boot_option:ramdisk'
        node.provision_state = states.DEPLOYING
        node.instance_info = {}
        node.save()
        with task_manager.acquire(self.context, node.uuid) as task:
            task.driver.deploy.prepare(task)
            self.assertFalse(mock_prepare_instance.called)
            self.assertEqual({'boot_option': 'ramdisk'},
                             task.node.instance_info['capabilities'])
            self.assertTrue(mock_warning.called)

    @mock.patch.object(deploy_utils, 'validate_image_properties',
                       autospec=True)
    def test_validate(self, mock_validate_img):
        node = self.node
        node.properties['capabilities'] = 'boot_option:netboot'
        node.save()
        with task_manager.acquire(self.context, node.uuid) as task:
            task.driver.deploy.validate(task)
        self.assertTrue(mock_validate_img.called)

    @mock.patch.object(deploy_utils, 'validate_image_properties',
                       autospec=True)
    def test_validate_interface_mismatch(self, mock_validate_image):
        node = self.node
        node.boot_interface = 'fake'
        node.save()
        self.config(enabled_boot_interfaces=['fake'],
                    default_boot_interface='fake')
        with task_manager.acquire(self.context, node.uuid) as task:
            self.assertRaisesRegexp(exception.InvalidParameterValue,
                                    'must have the `ramdisk_boot` capability',
                                    task.driver.deploy.validate, task)
            self.assertFalse(mock_validate_image.called)

    @mock.patch.object(pxe.PXEBoot, 'validate', autospec=True)
    def test_validate_calls_boot_validate(self, mock_validate):
        with task_manager.acquire(self.context, self.node.uuid) as task:
            task.driver.deploy.validate(task)
            mock_validate.assert_called_once_with(mock.ANY, task)


class PXEValidateRescueTestCase(db_base.DbTestCase):

    def setUp(self):
        super(PXEValidateRescueTestCase, self).setUp()
        for iface in drivers_base.ALL_INTERFACES:
            impl = 'fake'
            if iface == 'network':
                impl = 'flat'
            if iface == 'rescue':
                impl = 'agent'
            if iface == 'boot':
                impl = 'pxe'
            config_kwarg = {'enabled_%s_interfaces' % iface: [impl],
                            'default_%s_interface' % iface: impl}
            self.config(**config_kwarg)
        self.config(enabled_hardware_types=['fake-hardware'])
        driver_info = DRV_INFO_DICT
        driver_info.update({'rescue_ramdisk': 'my_ramdisk',
                            'rescue_kernel': 'my_kernel'})
        instance_info = INST_INFO_DICT
        instance_info.update({'rescue_password': 'password'})
        n = {
            'driver': 'fake-hardware',
            'instance_info': instance_info,
            'driver_info': driver_info,
            'driver_internal_info': DRV_INTERNAL_INFO_DICT,
        }
        self.node = obj_utils.create_test_node(self.context, **n)

    def test_validate_rescue(self):
        with task_manager.acquire(self.context, self.node.uuid) as task:
            task.driver.boot.validate_rescue(task)

    def test_validate_rescue_no_rescue_ramdisk(self):
        driver_info = self.node.driver_info
        del driver_info['rescue_ramdisk']
        self.node.driver_info = driver_info
        self.node.save()
        with task_manager.acquire(self.context, self.node.uuid) as task:
            self.assertRaisesRegex(exception.MissingParameterValue,
                                   'Missing.*rescue_ramdisk',
                                   task.driver.boot.validate_rescue, task)

    def test_validate_rescue_fails_no_rescue_kernel(self):
        driver_info = self.node.driver_info
        del driver_info['rescue_kernel']
        self.node.driver_info = driver_info
        self.node.save()
        with task_manager.acquire(self.context, self.node.uuid) as task:
            self.assertRaisesRegex(exception.MissingParameterValue,
                                   'Missing.*rescue_kernel',
                                   task.driver.boot.validate_rescue, task)


class TFTPImageCacheTestCase(db_base.DbTestCase):
    @mock.patch.object(fileutils, 'ensure_tree')
    def test_with_master_path(self, mock_ensure_tree):
        self.config(tftp_master_path='/fake/path', group='pxe')
        self.config(image_cache_size=500, group='pxe')
        self.config(image_cache_ttl=30, group='pxe')

        cache = pxe.TFTPImageCache()

        mock_ensure_tree.assert_called_once_with('/fake/path')
        self.assertEqual(500 * 1024 * 1024, cache._cache_size)
        self.assertEqual(30 * 60, cache._cache_ttl)

    @mock.patch.object(fileutils, 'ensure_tree')
    def test_without_master_path(self, mock_ensure_tree):
        self.config(tftp_master_path='', group='pxe')
        self.config(image_cache_size=500, group='pxe')
        self.config(image_cache_ttl=30, group='pxe')

        cache = pxe.TFTPImageCache()

        mock_ensure_tree.assert_not_called()
        self.assertEqual(500 * 1024 * 1024, cache._cache_size)
        self.assertEqual(30 * 60, cache._cache_ttl)
