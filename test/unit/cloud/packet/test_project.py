"""Unit tests for the packet project module."""
from cloud.packet import packet_project
import mock
import fixtures


class TestProject(object):
    @mock.patch.object(packet_project.AnsibleModule, 'fail_json')
    @mock.patch.object(packet_project.AnsibleModule, 'exit_json',
                       side_effect=fixtures.AnsibleExitOk)
    @mock.patch.object(packet_project.PacketModule,
    'manager', new_callable=mock.PropertyMock)
    @mock.patch.object(packet_project.AnsibleModule,
    '_load_params', autospec=True)
    def test_project_add(self,  mock_params, mock_manager_property, mock_exit,
                         mock_fail):
        """
        - packet_project:
            name: foo
            state: present
            auth_token: XYZ
        """
        mock_params.side_effect = fixtures.param_setter_from_doc(
            'packet_project', self.test_project_add)

        mock_manager_property.return_value = fixtures.Manager()

        try:
            packet_project.main()
        except fixtures.AnsibleExitOk:
            pass
        assert(mock_exit.call_count == 1)
        assert(mock_exit.call_args[1]['changed'])


    @mock.patch('packet.Project.Project')
    @mock.patch.object(packet_project.AnsibleModule, 'fail_json')
    @mock.patch.object(packet_project.AnsibleModule, 'exit_json',
                       side_effect=fixtures.AnsibleExitOk)
    @mock.patch.object(packet_project.PacketModule,
    'manager', new_callable=mock.PropertyMock)
    @mock.patch.object(packet_project.AnsibleModule,
    '_load_params', autospec=True)
    def test_project_exists(self,  mock_params, mock_manager_property,
                            mock_exit, mock_fail, mock_proj):
        """
        - packet_project:
            name: bar
            state: present
            auth_token: XYZ
        """
        mock_params.side_effect = fixtures.param_setter_from_doc(
            'packet_project', self.test_project_exists)
        project = mock_proj()
        project.name = 'bar'
        manager = fixtures.Manager()
        manager.projects.append(project)
        mock_manager_property.return_value = manager

        try:
            packet_project.main()
        except fixtures.AnsibleExitOk:
            pass
        assert(mock_exit.call_count == 1)
        assert(not mock_exit.call_args[1]['changed'])

    @mock.patch('packet.Project.Project')
    @mock.patch.object(packet_project.AnsibleModule, 'fail_json')
    @mock.patch.object(packet_project.AnsibleModule, 'exit_json',
                       side_effect=fixtures.AnsibleExitOk)
    @mock.patch.object(packet_project.PacketModule,
    'manager', new_callable=mock.PropertyMock)
    @mock.patch.object(packet_project.AnsibleModule,
    '_load_params', autospec=True)
    def test_project_delete(self,  mock_params, mock_manager_property,
                            mock_exit, mock_fail, mock_proj):
        """
        - packet_project:
            name: foo
            state: absent
            auth_token: XYZ
        """
        mock_params.side_effect = fixtures.param_setter_from_doc(
            'packet_project', self.test_project_delete)
        project = mock_proj()
        mock_proj.delete = mock.Mock()
        project.name = 'foo'
        manager = fixtures.Manager()
        manager.projects.append(project)
        mock_manager_property.return_value = manager

        try:
            packet_project.main()
        except fixtures.AnsibleExitOk:
            pass

        assert(mock_exit.call_count == 1)
        assert(mock_exit.call_args[1]['changed'])
        assert(project.delete.call_count == 1)

    @mock.patch.object(packet_project.AnsibleModule, 'fail_json')
    @mock.patch.object(packet_project.AnsibleModule, 'exit_json',
                       side_effect=fixtures.AnsibleExitOk)
    @mock.patch.object(packet_project.PacketModule,
    'manager', new_callable=mock.PropertyMock)
    @mock.patch.object(packet_project.AnsibleModule,
    '_load_params', autospec=True)
    def test_project_absent(self,  mock_params, mock_manager_property, mock_exit,
                         mock_fail):
        """
        - packet_project:
            name: foo
            state: absent
            auth_token: XYZ
        """
        mock_params.side_effect = fixtures.param_setter_from_doc(
            'packet_project', self.test_project_absent)

        mock_manager_property.return_value = fixtures.Manager()

        try:
            packet_project.main()
        except fixtures.AnsibleExitOk:
            pass
        assert(mock_exit.call_count == 1)
        assert(not mock_exit.call_args[1]['changed'])
