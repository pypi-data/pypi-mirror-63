# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

from admobilize.proto.devicemanagement.v1alpha3 import device_manager_pb2 as admobilize_dot_devicemanagement_dot_v1alpha3_dot_device__manager__pb2
from admobilize.proto.devicemanagement.v1alpha3 import resources_pb2 as admobilize_dot_devicemanagement_dot_v1alpha3_dot_resources__pb2
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2


class DeviceManagerStub(object):
  """API design guide: https://cloud.google.com/apis/design/

  The service that an application uses to create, update, delete, manipulate and obtain
  devices.

  [START device management service]
  """

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.CreateDevice = channel.unary_unary(
        '/admobilize.devicemanagement.v1alpha3.DeviceManager/CreateDevice',
        request_serializer=admobilize_dot_devicemanagement_dot_v1alpha3_dot_device__manager__pb2.CreateDeviceRequest.SerializeToString,
        response_deserializer=admobilize_dot_devicemanagement_dot_v1alpha3_dot_resources__pb2.Device.FromString,
        )
    self.GetDevice = channel.unary_unary(
        '/admobilize.devicemanagement.v1alpha3.DeviceManager/GetDevice',
        request_serializer=admobilize_dot_devicemanagement_dot_v1alpha3_dot_device__manager__pb2.GetDeviceRequest.SerializeToString,
        response_deserializer=admobilize_dot_devicemanagement_dot_v1alpha3_dot_resources__pb2.Device.FromString,
        )
    self.ListDevices = channel.unary_unary(
        '/admobilize.devicemanagement.v1alpha3.DeviceManager/ListDevices',
        request_serializer=admobilize_dot_devicemanagement_dot_v1alpha3_dot_device__manager__pb2.ListDevicesRequest.SerializeToString,
        response_deserializer=admobilize_dot_devicemanagement_dot_v1alpha3_dot_device__manager__pb2.ListDevicesResponse.FromString,
        )
    self.UpdateDevice = channel.unary_unary(
        '/admobilize.devicemanagement.v1alpha3.DeviceManager/UpdateDevice',
        request_serializer=admobilize_dot_devicemanagement_dot_v1alpha3_dot_device__manager__pb2.UpdateDeviceRequest.SerializeToString,
        response_deserializer=admobilize_dot_devicemanagement_dot_v1alpha3_dot_resources__pb2.Device.FromString,
        )
    self.DeleteDevice = channel.unary_unary(
        '/admobilize.devicemanagement.v1alpha3.DeviceManager/DeleteDevice',
        request_serializer=admobilize_dot_devicemanagement_dot_v1alpha3_dot_device__manager__pb2.DeleteDeviceRequest.SerializeToString,
        response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
        )
    self.InstallApplication = channel.unary_unary(
        '/admobilize.devicemanagement.v1alpha3.DeviceManager/InstallApplication',
        request_serializer=admobilize_dot_devicemanagement_dot_v1alpha3_dot_device__manager__pb2.InstallApplicationRequest.SerializeToString,
        response_deserializer=admobilize_dot_devicemanagement_dot_v1alpha3_dot_resources__pb2.Device.FromString,
        )
    self.CreateProject = channel.unary_unary(
        '/admobilize.devicemanagement.v1alpha3.DeviceManager/CreateProject',
        request_serializer=admobilize_dot_devicemanagement_dot_v1alpha3_dot_resources__pb2.Project.SerializeToString,
        response_deserializer=admobilize_dot_devicemanagement_dot_v1alpha3_dot_resources__pb2.Project.FromString,
        )
    self.GetProject = channel.unary_unary(
        '/admobilize.devicemanagement.v1alpha3.DeviceManager/GetProject',
        request_serializer=admobilize_dot_devicemanagement_dot_v1alpha3_dot_device__manager__pb2.GetProjectRequest.SerializeToString,
        response_deserializer=admobilize_dot_devicemanagement_dot_v1alpha3_dot_resources__pb2.Project.FromString,
        )
    self.ListProjects = channel.unary_unary(
        '/admobilize.devicemanagement.v1alpha3.DeviceManager/ListProjects',
        request_serializer=admobilize_dot_devicemanagement_dot_v1alpha3_dot_device__manager__pb2.ListProjectsRequest.SerializeToString,
        response_deserializer=admobilize_dot_devicemanagement_dot_v1alpha3_dot_device__manager__pb2.ListProjectsResponse.FromString,
        )
    self.UpdateProject = channel.unary_unary(
        '/admobilize.devicemanagement.v1alpha3.DeviceManager/UpdateProject',
        request_serializer=admobilize_dot_devicemanagement_dot_v1alpha3_dot_device__manager__pb2.UpdateProjectRequest.SerializeToString,
        response_deserializer=admobilize_dot_devicemanagement_dot_v1alpha3_dot_resources__pb2.Project.FromString,
        )
    self.DeleteProject = channel.unary_unary(
        '/admobilize.devicemanagement.v1alpha3.DeviceManager/DeleteProject',
        request_serializer=admobilize_dot_devicemanagement_dot_v1alpha3_dot_device__manager__pb2.DeleteProjectRequest.SerializeToString,
        response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
        )
    self.AddProjectUser = channel.unary_unary(
        '/admobilize.devicemanagement.v1alpha3.DeviceManager/AddProjectUser',
        request_serializer=admobilize_dot_devicemanagement_dot_v1alpha3_dot_device__manager__pb2.AddProjectUserRequest.SerializeToString,
        response_deserializer=admobilize_dot_devicemanagement_dot_v1alpha3_dot_resources__pb2.Project.FromString,
        )
    self.GenerateProvisioningToken = channel.unary_unary(
        '/admobilize.devicemanagement.v1alpha3.DeviceManager/GenerateProvisioningToken',
        request_serializer=admobilize_dot_devicemanagement_dot_v1alpha3_dot_device__manager__pb2.GenerateProvisioningTokenRequest.SerializeToString,
        response_deserializer=admobilize_dot_devicemanagement_dot_v1alpha3_dot_device__manager__pb2.GenerateProvisioningTokenResponse.FromString,
        )
    self.RemoveProjectUser = channel.unary_unary(
        '/admobilize.devicemanagement.v1alpha3.DeviceManager/RemoveProjectUser',
        request_serializer=admobilize_dot_devicemanagement_dot_v1alpha3_dot_device__manager__pb2.RemoveProjectUserRequest.SerializeToString,
        response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
        )
    self.MoveDevice = channel.unary_unary(
        '/admobilize.devicemanagement.v1alpha3.DeviceManager/MoveDevice',
        request_serializer=admobilize_dot_devicemanagement_dot_v1alpha3_dot_device__manager__pb2.MoveDeviceRequest.SerializeToString,
        response_deserializer=admobilize_dot_devicemanagement_dot_v1alpha3_dot_resources__pb2.Project.FromString,
        )
    self.SendCommandToDevice = channel.unary_unary(
        '/admobilize.devicemanagement.v1alpha3.DeviceManager/SendCommandToDevice',
        request_serializer=admobilize_dot_devicemanagement_dot_v1alpha3_dot_device__manager__pb2.SendCommandToDeviceRequest.SerializeToString,
        response_deserializer=admobilize_dot_devicemanagement_dot_v1alpha3_dot_device__manager__pb2.SendCommandToDeviceResponse.FromString,
        )
    self.BatchCreateDevices = channel.unary_unary(
        '/admobilize.devicemanagement.v1alpha3.DeviceManager/BatchCreateDevices',
        request_serializer=admobilize_dot_devicemanagement_dot_v1alpha3_dot_device__manager__pb2.BatchCreateDevicesRequest.SerializeToString,
        response_deserializer=admobilize_dot_devicemanagement_dot_v1alpha3_dot_device__manager__pb2.BatchCreateDevicesResponse.FromString,
        )
    self.ArchiveDevice = channel.unary_unary(
        '/admobilize.devicemanagement.v1alpha3.DeviceManager/ArchiveDevice',
        request_serializer=admobilize_dot_devicemanagement_dot_v1alpha3_dot_device__manager__pb2.ArchiveDeviceRequest.SerializeToString,
        response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
        )
    self.DearchiveDevice = channel.unary_unary(
        '/admobilize.devicemanagement.v1alpha3.DeviceManager/DearchiveDevice',
        request_serializer=admobilize_dot_devicemanagement_dot_v1alpha3_dot_device__manager__pb2.DearchiveDeviceRequest.SerializeToString,
        response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
        )
    self.ProvisionDevices = channel.unary_unary(
        '/admobilize.devicemanagement.v1alpha3.DeviceManager/ProvisionDevices',
        request_serializer=admobilize_dot_devicemanagement_dot_v1alpha3_dot_device__manager__pb2.ProvisionDevicesRequest.SerializeToString,
        response_deserializer=admobilize_dot_devicemanagement_dot_v1alpha3_dot_device__manager__pb2.ProvisionDevicesResponse.FromString,
        )
    self.VerifyDeviceToken = channel.unary_unary(
        '/admobilize.devicemanagement.v1alpha3.DeviceManager/VerifyDeviceToken',
        request_serializer=admobilize_dot_devicemanagement_dot_v1alpha3_dot_device__manager__pb2.VerifyDeviceTokenRequest.SerializeToString,
        response_deserializer=admobilize_dot_devicemanagement_dot_v1alpha3_dot_resources__pb2.Device.FromString,
        )


class DeviceManagerServicer(object):
  """API design guide: https://cloud.google.com/apis/design/

  The service that an application uses to create, update, delete, manipulate and obtain
  devices.

  [START device management service]
  """

  def CreateDevice(self, request, context):
    """--- Standard methods -----------------------------------------------------------

    Creates a device
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def GetDevice(self, request, context):
    """Gets a device
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def ListDevices(self, request, context):
    """Lists devices in a project
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def UpdateDevice(self, request, context):
    """Updates a device
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def DeleteDevice(self, request, context):
    """Deletes a device
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def InstallApplication(self, request, context):
    """Installs an application on a device
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def CreateProject(self, request, context):
    """Creates a project
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def GetProject(self, request, context):
    """Gets a project
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def ListProjects(self, request, context):
    """List the projects to which the current authenticated user has access to
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def UpdateProject(self, request, context):
    """Updates a project
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def DeleteProject(self, request, context):
    """Deletes a project
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def AddProjectUser(self, request, context):
    """--- Custom methods -----------------------------------------------------------

    Add user to project
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def GenerateProvisioningToken(self, request, context):
    """Generate a new provisioning token for a device
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def RemoveProjectUser(self, request, context):
    """Remove user from project
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def MoveDevice(self, request, context):
    """Move device from one project to another
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def SendCommandToDevice(self, request, context):
    """Send command to device
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def BatchCreateDevices(self, request, context):
    """Create many devices at once
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def ArchiveDevice(self, request, context):
    """Achives a device
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def DearchiveDevice(self, request, context):
    """Dearchives a device
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def ProvisionDevices(self, request, context):
    """Provision devices
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def VerifyDeviceToken(self, request, context):
    """Validates if a given token is a legitimate device token, this is
    the signature matches the registered public key
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_DeviceManagerServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'CreateDevice': grpc.unary_unary_rpc_method_handler(
          servicer.CreateDevice,
          request_deserializer=admobilize_dot_devicemanagement_dot_v1alpha3_dot_device__manager__pb2.CreateDeviceRequest.FromString,
          response_serializer=admobilize_dot_devicemanagement_dot_v1alpha3_dot_resources__pb2.Device.SerializeToString,
      ),
      'GetDevice': grpc.unary_unary_rpc_method_handler(
          servicer.GetDevice,
          request_deserializer=admobilize_dot_devicemanagement_dot_v1alpha3_dot_device__manager__pb2.GetDeviceRequest.FromString,
          response_serializer=admobilize_dot_devicemanagement_dot_v1alpha3_dot_resources__pb2.Device.SerializeToString,
      ),
      'ListDevices': grpc.unary_unary_rpc_method_handler(
          servicer.ListDevices,
          request_deserializer=admobilize_dot_devicemanagement_dot_v1alpha3_dot_device__manager__pb2.ListDevicesRequest.FromString,
          response_serializer=admobilize_dot_devicemanagement_dot_v1alpha3_dot_device__manager__pb2.ListDevicesResponse.SerializeToString,
      ),
      'UpdateDevice': grpc.unary_unary_rpc_method_handler(
          servicer.UpdateDevice,
          request_deserializer=admobilize_dot_devicemanagement_dot_v1alpha3_dot_device__manager__pb2.UpdateDeviceRequest.FromString,
          response_serializer=admobilize_dot_devicemanagement_dot_v1alpha3_dot_resources__pb2.Device.SerializeToString,
      ),
      'DeleteDevice': grpc.unary_unary_rpc_method_handler(
          servicer.DeleteDevice,
          request_deserializer=admobilize_dot_devicemanagement_dot_v1alpha3_dot_device__manager__pb2.DeleteDeviceRequest.FromString,
          response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
      ),
      'InstallApplication': grpc.unary_unary_rpc_method_handler(
          servicer.InstallApplication,
          request_deserializer=admobilize_dot_devicemanagement_dot_v1alpha3_dot_device__manager__pb2.InstallApplicationRequest.FromString,
          response_serializer=admobilize_dot_devicemanagement_dot_v1alpha3_dot_resources__pb2.Device.SerializeToString,
      ),
      'CreateProject': grpc.unary_unary_rpc_method_handler(
          servicer.CreateProject,
          request_deserializer=admobilize_dot_devicemanagement_dot_v1alpha3_dot_resources__pb2.Project.FromString,
          response_serializer=admobilize_dot_devicemanagement_dot_v1alpha3_dot_resources__pb2.Project.SerializeToString,
      ),
      'GetProject': grpc.unary_unary_rpc_method_handler(
          servicer.GetProject,
          request_deserializer=admobilize_dot_devicemanagement_dot_v1alpha3_dot_device__manager__pb2.GetProjectRequest.FromString,
          response_serializer=admobilize_dot_devicemanagement_dot_v1alpha3_dot_resources__pb2.Project.SerializeToString,
      ),
      'ListProjects': grpc.unary_unary_rpc_method_handler(
          servicer.ListProjects,
          request_deserializer=admobilize_dot_devicemanagement_dot_v1alpha3_dot_device__manager__pb2.ListProjectsRequest.FromString,
          response_serializer=admobilize_dot_devicemanagement_dot_v1alpha3_dot_device__manager__pb2.ListProjectsResponse.SerializeToString,
      ),
      'UpdateProject': grpc.unary_unary_rpc_method_handler(
          servicer.UpdateProject,
          request_deserializer=admobilize_dot_devicemanagement_dot_v1alpha3_dot_device__manager__pb2.UpdateProjectRequest.FromString,
          response_serializer=admobilize_dot_devicemanagement_dot_v1alpha3_dot_resources__pb2.Project.SerializeToString,
      ),
      'DeleteProject': grpc.unary_unary_rpc_method_handler(
          servicer.DeleteProject,
          request_deserializer=admobilize_dot_devicemanagement_dot_v1alpha3_dot_device__manager__pb2.DeleteProjectRequest.FromString,
          response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
      ),
      'AddProjectUser': grpc.unary_unary_rpc_method_handler(
          servicer.AddProjectUser,
          request_deserializer=admobilize_dot_devicemanagement_dot_v1alpha3_dot_device__manager__pb2.AddProjectUserRequest.FromString,
          response_serializer=admobilize_dot_devicemanagement_dot_v1alpha3_dot_resources__pb2.Project.SerializeToString,
      ),
      'GenerateProvisioningToken': grpc.unary_unary_rpc_method_handler(
          servicer.GenerateProvisioningToken,
          request_deserializer=admobilize_dot_devicemanagement_dot_v1alpha3_dot_device__manager__pb2.GenerateProvisioningTokenRequest.FromString,
          response_serializer=admobilize_dot_devicemanagement_dot_v1alpha3_dot_device__manager__pb2.GenerateProvisioningTokenResponse.SerializeToString,
      ),
      'RemoveProjectUser': grpc.unary_unary_rpc_method_handler(
          servicer.RemoveProjectUser,
          request_deserializer=admobilize_dot_devicemanagement_dot_v1alpha3_dot_device__manager__pb2.RemoveProjectUserRequest.FromString,
          response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
      ),
      'MoveDevice': grpc.unary_unary_rpc_method_handler(
          servicer.MoveDevice,
          request_deserializer=admobilize_dot_devicemanagement_dot_v1alpha3_dot_device__manager__pb2.MoveDeviceRequest.FromString,
          response_serializer=admobilize_dot_devicemanagement_dot_v1alpha3_dot_resources__pb2.Project.SerializeToString,
      ),
      'SendCommandToDevice': grpc.unary_unary_rpc_method_handler(
          servicer.SendCommandToDevice,
          request_deserializer=admobilize_dot_devicemanagement_dot_v1alpha3_dot_device__manager__pb2.SendCommandToDeviceRequest.FromString,
          response_serializer=admobilize_dot_devicemanagement_dot_v1alpha3_dot_device__manager__pb2.SendCommandToDeviceResponse.SerializeToString,
      ),
      'BatchCreateDevices': grpc.unary_unary_rpc_method_handler(
          servicer.BatchCreateDevices,
          request_deserializer=admobilize_dot_devicemanagement_dot_v1alpha3_dot_device__manager__pb2.BatchCreateDevicesRequest.FromString,
          response_serializer=admobilize_dot_devicemanagement_dot_v1alpha3_dot_device__manager__pb2.BatchCreateDevicesResponse.SerializeToString,
      ),
      'ArchiveDevice': grpc.unary_unary_rpc_method_handler(
          servicer.ArchiveDevice,
          request_deserializer=admobilize_dot_devicemanagement_dot_v1alpha3_dot_device__manager__pb2.ArchiveDeviceRequest.FromString,
          response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
      ),
      'DearchiveDevice': grpc.unary_unary_rpc_method_handler(
          servicer.DearchiveDevice,
          request_deserializer=admobilize_dot_devicemanagement_dot_v1alpha3_dot_device__manager__pb2.DearchiveDeviceRequest.FromString,
          response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
      ),
      'ProvisionDevices': grpc.unary_unary_rpc_method_handler(
          servicer.ProvisionDevices,
          request_deserializer=admobilize_dot_devicemanagement_dot_v1alpha3_dot_device__manager__pb2.ProvisionDevicesRequest.FromString,
          response_serializer=admobilize_dot_devicemanagement_dot_v1alpha3_dot_device__manager__pb2.ProvisionDevicesResponse.SerializeToString,
      ),
      'VerifyDeviceToken': grpc.unary_unary_rpc_method_handler(
          servicer.VerifyDeviceToken,
          request_deserializer=admobilize_dot_devicemanagement_dot_v1alpha3_dot_device__manager__pb2.VerifyDeviceTokenRequest.FromString,
          response_serializer=admobilize_dot_devicemanagement_dot_v1alpha3_dot_resources__pb2.Device.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'admobilize.devicemanagement.v1alpha3.DeviceManager', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
