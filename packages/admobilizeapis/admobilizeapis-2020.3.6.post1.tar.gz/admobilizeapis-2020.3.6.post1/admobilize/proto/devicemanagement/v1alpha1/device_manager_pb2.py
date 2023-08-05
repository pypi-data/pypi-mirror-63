# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: admobilize/devicemanagement/v1alpha1/device_manager.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from google.protobuf import field_mask_pb2 as google_dot_protobuf_dot_field__mask__pb2
from admobilize.proto.devicemanagement.v1alpha1 import resources_pb2 as admobilize_dot_devicemanagement_dot_v1alpha1_dot_resources__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='admobilize/devicemanagement/v1alpha1/device_manager.proto',
  package='admobilize.devicemanagement.v1alpha1',
  syntax='proto3',
  serialized_options=b'\n(com.admobilize.devicemanagement.v1alpha1B\022DeviceManagerProtoP\001ZHbitbucket.org/admobilize/admobilizeapis-go/pkg/devicemanagement/v1alpha1\242\002\005ADMDM\252\002$AdMobilize.DeviceManagement.V1Alpha1',
  serialized_pb=b'\n9admobilize/devicemanagement/v1alpha1/device_manager.proto\x12$admobilize.devicemanagement.v1alpha1\x1a\x1cgoogle/api/annotations.proto\x1a\x1bgoogle/protobuf/empty.proto\x1a google/protobuf/field_mask.proto\x1a\x34\x61\x64mobilize/devicemanagement/v1alpha1/resources.proto\"N\n\x10GetDeviceRequest\x12\n\n\x02id\x18\x01 \x01(\t\x12.\n\nfield_mask\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.FieldMask\"{\n\x12ListDevicesRequest\x12\x0e\n\x06parent\x18\x01 \x01(\t\x12.\n\nfield_mask\x18\x04 \x01(\x0b\x32\x1a.google.protobuf.FieldMask\x12\x11\n\tpage_size\x18\x64 \x01(\x05\x12\x12\n\npage_token\x18\x65 \x01(\t\"m\n\x13ListDevicesResponse\x12=\n\x07\x64\x65vices\x18\x01 \x03(\x0b\x32,.admobilize.devicemanagement.v1alpha1.Device\x12\x17\n\x0fnext_page_token\x18\x02 \x01(\t\"\x84\x01\n\x13UpdateDeviceRequest\x12<\n\x06\x64\x65vice\x18\x01 \x01(\x0b\x32,.admobilize.devicemanagement.v1alpha1.Device\x12/\n\x0bupdate_mask\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.FieldMask\"!\n\x13\x44\x65leteDeviceRequest\x12\n\n\x02id\x18\x01 \x01(\t\"O\n\x11GetProjectRequest\x12\n\n\x02id\x18\x01 \x01(\t\x12.\n\nfield_mask\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.FieldMask\"l\n\x13ListProjectsRequest\x12.\n\nfield_mask\x18\x01 \x01(\x0b\x32\x1a.google.protobuf.FieldMask\x12\x11\n\tpage_size\x18\x64 \x01(\x05\x12\x12\n\npage_token\x18\x65 \x01(\t\"p\n\x14ListProjectsResponse\x12?\n\x08projects\x18\x01 \x03(\x0b\x32-.admobilize.devicemanagement.v1alpha1.Project\x12\x17\n\x0fnext_page_token\x18\x02 \x01(\t\"\x87\x01\n\x14UpdateProjectRequest\x12>\n\x07project\x18\x01 \x01(\x0b\x32-.admobilize.devicemanagement.v1alpha1.Project\x12/\n\x0bupdate_mask\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.FieldMask\"\"\n\x14\x44\x65leteProjectRequest\x12\n\n\x02id\x18\x01 \x01(\t\"Z\n\x19\x42\x61tchCreateDevicesRequest\x12=\n\x07\x64\x65vices\x18\x01 \x03(\x0b\x32,.admobilize.devicemanagement.v1alpha1.Device\"[\n\x1a\x42\x61tchCreateDevicesResponse\x12=\n\x07\x64\x65vices\x18\x01 \x03(\x0b\x32,.admobilize.devicemanagement.v1alpha1.Device\"X\n\x17ProvisionDevicesRequest\x12=\n\x07\x64\x65vices\x18\x01 \x03(\x0b\x32,.admobilize.devicemanagement.v1alpha1.Device\"Y\n\x18ProvisionDevicesResponse\x12=\n\x07\x64\x65vices\x18\x01 \x03(\x0b\x32,.admobilize.devicemanagement.v1alpha1.Device\")\n\x18VerifyDeviceTokenRequest\x12\r\n\x05token\x18\x01 \x01(\t2\xe8\x08\n\rDeviceManager\x12\x88\x01\n\x0c\x43reateDevice\x12,.admobilize.devicemanagement.v1alpha1.Device\x1a,.admobilize.devicemanagement.v1alpha1.Device\"\x1c\x82\xd3\xe4\x93\x02\x16\"\x11/v1alpha1/devices:\x01*\x12\x93\x01\n\tGetDevice\x12\x36.admobilize.devicemanagement.v1alpha1.GetDeviceRequest\x1a,.admobilize.devicemanagement.v1alpha1.Device\" \x82\xd3\xe4\x93\x02\x1a\x12\x18/v1alpha1/{id=devices/*}\x12\x9d\x01\n\x0bListDevices\x12\x38.admobilize.devicemanagement.v1alpha1.ListDevicesRequest\x1a\x39.admobilize.devicemanagement.v1alpha1.ListDevicesResponse\"\x19\x82\xd3\xe4\x93\x02\x13\x12\x11/v1alpha1/devices\x12\xa8\x01\n\x0cUpdateDevice\x12\x39.admobilize.devicemanagement.v1alpha1.UpdateDeviceRequest\x1a,.admobilize.devicemanagement.v1alpha1.Device\"/\x82\xd3\xe4\x93\x02)2\x1f/v1alpha1/{device.id=devices/*}:\x06\x64\x65vice\x12\x83\x01\n\x0c\x44\x65leteDevice\x12\x39.admobilize.devicemanagement.v1alpha1.DeleteDeviceRequest\x1a\x16.google.protobuf.Empty\" \x82\xd3\xe4\x93\x02\x1a*\x18/v1alpha1/{id=devices/*}\x12\xb9\x01\n\x10ProvisionDevices\x12=.admobilize.devicemanagement.v1alpha1.ProvisionDevicesRequest\x1a>.admobilize.devicemanagement.v1alpha1.ProvisionDevicesResponse\"&\x82\xd3\xe4\x93\x02 2\x1b/v1alpha1/devices/provision:\x01*\x12\xa8\x01\n\x11VerifyDeviceToken\x12>.admobilize.devicemanagement.v1alpha1.VerifyDeviceTokenRequest\x1a,.admobilize.devicemanagement.v1alpha1.Device\"%\x82\xd3\xe4\x93\x02\x1f\x12\x1d/v1alpha1/devicetokens/verifyB\xb9\x01\n(com.admobilize.devicemanagement.v1alpha1B\x12\x44\x65viceManagerProtoP\x01ZHbitbucket.org/admobilize/admobilizeapis-go/pkg/devicemanagement/v1alpha1\xa2\x02\x05\x41\x44MDM\xaa\x02$AdMobilize.DeviceManagement.V1Alpha1b\x06proto3'
  ,
  dependencies=[google_dot_api_dot_annotations__pb2.DESCRIPTOR,google_dot_protobuf_dot_empty__pb2.DESCRIPTOR,google_dot_protobuf_dot_field__mask__pb2.DESCRIPTOR,admobilize_dot_devicemanagement_dot_v1alpha1_dot_resources__pb2.DESCRIPTOR,])




_GETDEVICEREQUEST = _descriptor.Descriptor(
  name='GetDeviceRequest',
  full_name='admobilize.devicemanagement.v1alpha1.GetDeviceRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='admobilize.devicemanagement.v1alpha1.GetDeviceRequest.id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='field_mask', full_name='admobilize.devicemanagement.v1alpha1.GetDeviceRequest.field_mask', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=246,
  serialized_end=324,
)


_LISTDEVICESREQUEST = _descriptor.Descriptor(
  name='ListDevicesRequest',
  full_name='admobilize.devicemanagement.v1alpha1.ListDevicesRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='parent', full_name='admobilize.devicemanagement.v1alpha1.ListDevicesRequest.parent', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='field_mask', full_name='admobilize.devicemanagement.v1alpha1.ListDevicesRequest.field_mask', index=1,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='page_size', full_name='admobilize.devicemanagement.v1alpha1.ListDevicesRequest.page_size', index=2,
      number=100, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='page_token', full_name='admobilize.devicemanagement.v1alpha1.ListDevicesRequest.page_token', index=3,
      number=101, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=326,
  serialized_end=449,
)


_LISTDEVICESRESPONSE = _descriptor.Descriptor(
  name='ListDevicesResponse',
  full_name='admobilize.devicemanagement.v1alpha1.ListDevicesResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='devices', full_name='admobilize.devicemanagement.v1alpha1.ListDevicesResponse.devices', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='next_page_token', full_name='admobilize.devicemanagement.v1alpha1.ListDevicesResponse.next_page_token', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=451,
  serialized_end=560,
)


_UPDATEDEVICEREQUEST = _descriptor.Descriptor(
  name='UpdateDeviceRequest',
  full_name='admobilize.devicemanagement.v1alpha1.UpdateDeviceRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='device', full_name='admobilize.devicemanagement.v1alpha1.UpdateDeviceRequest.device', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='update_mask', full_name='admobilize.devicemanagement.v1alpha1.UpdateDeviceRequest.update_mask', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=563,
  serialized_end=695,
)


_DELETEDEVICEREQUEST = _descriptor.Descriptor(
  name='DeleteDeviceRequest',
  full_name='admobilize.devicemanagement.v1alpha1.DeleteDeviceRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='admobilize.devicemanagement.v1alpha1.DeleteDeviceRequest.id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=697,
  serialized_end=730,
)


_GETPROJECTREQUEST = _descriptor.Descriptor(
  name='GetProjectRequest',
  full_name='admobilize.devicemanagement.v1alpha1.GetProjectRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='admobilize.devicemanagement.v1alpha1.GetProjectRequest.id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='field_mask', full_name='admobilize.devicemanagement.v1alpha1.GetProjectRequest.field_mask', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=732,
  serialized_end=811,
)


_LISTPROJECTSREQUEST = _descriptor.Descriptor(
  name='ListProjectsRequest',
  full_name='admobilize.devicemanagement.v1alpha1.ListProjectsRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='field_mask', full_name='admobilize.devicemanagement.v1alpha1.ListProjectsRequest.field_mask', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='page_size', full_name='admobilize.devicemanagement.v1alpha1.ListProjectsRequest.page_size', index=1,
      number=100, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='page_token', full_name='admobilize.devicemanagement.v1alpha1.ListProjectsRequest.page_token', index=2,
      number=101, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=813,
  serialized_end=921,
)


_LISTPROJECTSRESPONSE = _descriptor.Descriptor(
  name='ListProjectsResponse',
  full_name='admobilize.devicemanagement.v1alpha1.ListProjectsResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='projects', full_name='admobilize.devicemanagement.v1alpha1.ListProjectsResponse.projects', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='next_page_token', full_name='admobilize.devicemanagement.v1alpha1.ListProjectsResponse.next_page_token', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=923,
  serialized_end=1035,
)


_UPDATEPROJECTREQUEST = _descriptor.Descriptor(
  name='UpdateProjectRequest',
  full_name='admobilize.devicemanagement.v1alpha1.UpdateProjectRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='project', full_name='admobilize.devicemanagement.v1alpha1.UpdateProjectRequest.project', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='update_mask', full_name='admobilize.devicemanagement.v1alpha1.UpdateProjectRequest.update_mask', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1038,
  serialized_end=1173,
)


_DELETEPROJECTREQUEST = _descriptor.Descriptor(
  name='DeleteProjectRequest',
  full_name='admobilize.devicemanagement.v1alpha1.DeleteProjectRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='admobilize.devicemanagement.v1alpha1.DeleteProjectRequest.id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1175,
  serialized_end=1209,
)


_BATCHCREATEDEVICESREQUEST = _descriptor.Descriptor(
  name='BatchCreateDevicesRequest',
  full_name='admobilize.devicemanagement.v1alpha1.BatchCreateDevicesRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='devices', full_name='admobilize.devicemanagement.v1alpha1.BatchCreateDevicesRequest.devices', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1211,
  serialized_end=1301,
)


_BATCHCREATEDEVICESRESPONSE = _descriptor.Descriptor(
  name='BatchCreateDevicesResponse',
  full_name='admobilize.devicemanagement.v1alpha1.BatchCreateDevicesResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='devices', full_name='admobilize.devicemanagement.v1alpha1.BatchCreateDevicesResponse.devices', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1303,
  serialized_end=1394,
)


_PROVISIONDEVICESREQUEST = _descriptor.Descriptor(
  name='ProvisionDevicesRequest',
  full_name='admobilize.devicemanagement.v1alpha1.ProvisionDevicesRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='devices', full_name='admobilize.devicemanagement.v1alpha1.ProvisionDevicesRequest.devices', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1396,
  serialized_end=1484,
)


_PROVISIONDEVICESRESPONSE = _descriptor.Descriptor(
  name='ProvisionDevicesResponse',
  full_name='admobilize.devicemanagement.v1alpha1.ProvisionDevicesResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='devices', full_name='admobilize.devicemanagement.v1alpha1.ProvisionDevicesResponse.devices', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1486,
  serialized_end=1575,
)


_VERIFYDEVICETOKENREQUEST = _descriptor.Descriptor(
  name='VerifyDeviceTokenRequest',
  full_name='admobilize.devicemanagement.v1alpha1.VerifyDeviceTokenRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='token', full_name='admobilize.devicemanagement.v1alpha1.VerifyDeviceTokenRequest.token', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1577,
  serialized_end=1618,
)

_GETDEVICEREQUEST.fields_by_name['field_mask'].message_type = google_dot_protobuf_dot_field__mask__pb2._FIELDMASK
_LISTDEVICESREQUEST.fields_by_name['field_mask'].message_type = google_dot_protobuf_dot_field__mask__pb2._FIELDMASK
_LISTDEVICESRESPONSE.fields_by_name['devices'].message_type = admobilize_dot_devicemanagement_dot_v1alpha1_dot_resources__pb2._DEVICE
_UPDATEDEVICEREQUEST.fields_by_name['device'].message_type = admobilize_dot_devicemanagement_dot_v1alpha1_dot_resources__pb2._DEVICE
_UPDATEDEVICEREQUEST.fields_by_name['update_mask'].message_type = google_dot_protobuf_dot_field__mask__pb2._FIELDMASK
_GETPROJECTREQUEST.fields_by_name['field_mask'].message_type = google_dot_protobuf_dot_field__mask__pb2._FIELDMASK
_LISTPROJECTSREQUEST.fields_by_name['field_mask'].message_type = google_dot_protobuf_dot_field__mask__pb2._FIELDMASK
_LISTPROJECTSRESPONSE.fields_by_name['projects'].message_type = admobilize_dot_devicemanagement_dot_v1alpha1_dot_resources__pb2._PROJECT
_UPDATEPROJECTREQUEST.fields_by_name['project'].message_type = admobilize_dot_devicemanagement_dot_v1alpha1_dot_resources__pb2._PROJECT
_UPDATEPROJECTREQUEST.fields_by_name['update_mask'].message_type = google_dot_protobuf_dot_field__mask__pb2._FIELDMASK
_BATCHCREATEDEVICESREQUEST.fields_by_name['devices'].message_type = admobilize_dot_devicemanagement_dot_v1alpha1_dot_resources__pb2._DEVICE
_BATCHCREATEDEVICESRESPONSE.fields_by_name['devices'].message_type = admobilize_dot_devicemanagement_dot_v1alpha1_dot_resources__pb2._DEVICE
_PROVISIONDEVICESREQUEST.fields_by_name['devices'].message_type = admobilize_dot_devicemanagement_dot_v1alpha1_dot_resources__pb2._DEVICE
_PROVISIONDEVICESRESPONSE.fields_by_name['devices'].message_type = admobilize_dot_devicemanagement_dot_v1alpha1_dot_resources__pb2._DEVICE
DESCRIPTOR.message_types_by_name['GetDeviceRequest'] = _GETDEVICEREQUEST
DESCRIPTOR.message_types_by_name['ListDevicesRequest'] = _LISTDEVICESREQUEST
DESCRIPTOR.message_types_by_name['ListDevicesResponse'] = _LISTDEVICESRESPONSE
DESCRIPTOR.message_types_by_name['UpdateDeviceRequest'] = _UPDATEDEVICEREQUEST
DESCRIPTOR.message_types_by_name['DeleteDeviceRequest'] = _DELETEDEVICEREQUEST
DESCRIPTOR.message_types_by_name['GetProjectRequest'] = _GETPROJECTREQUEST
DESCRIPTOR.message_types_by_name['ListProjectsRequest'] = _LISTPROJECTSREQUEST
DESCRIPTOR.message_types_by_name['ListProjectsResponse'] = _LISTPROJECTSRESPONSE
DESCRIPTOR.message_types_by_name['UpdateProjectRequest'] = _UPDATEPROJECTREQUEST
DESCRIPTOR.message_types_by_name['DeleteProjectRequest'] = _DELETEPROJECTREQUEST
DESCRIPTOR.message_types_by_name['BatchCreateDevicesRequest'] = _BATCHCREATEDEVICESREQUEST
DESCRIPTOR.message_types_by_name['BatchCreateDevicesResponse'] = _BATCHCREATEDEVICESRESPONSE
DESCRIPTOR.message_types_by_name['ProvisionDevicesRequest'] = _PROVISIONDEVICESREQUEST
DESCRIPTOR.message_types_by_name['ProvisionDevicesResponse'] = _PROVISIONDEVICESRESPONSE
DESCRIPTOR.message_types_by_name['VerifyDeviceTokenRequest'] = _VERIFYDEVICETOKENREQUEST
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

GetDeviceRequest = _reflection.GeneratedProtocolMessageType('GetDeviceRequest', (_message.Message,), {
  'DESCRIPTOR' : _GETDEVICEREQUEST,
  '__module__' : 'admobilize.devicemanagement.v1alpha1.device_manager_pb2'
  # @@protoc_insertion_point(class_scope:admobilize.devicemanagement.v1alpha1.GetDeviceRequest)
  })
_sym_db.RegisterMessage(GetDeviceRequest)

ListDevicesRequest = _reflection.GeneratedProtocolMessageType('ListDevicesRequest', (_message.Message,), {
  'DESCRIPTOR' : _LISTDEVICESREQUEST,
  '__module__' : 'admobilize.devicemanagement.v1alpha1.device_manager_pb2'
  # @@protoc_insertion_point(class_scope:admobilize.devicemanagement.v1alpha1.ListDevicesRequest)
  })
_sym_db.RegisterMessage(ListDevicesRequest)

ListDevicesResponse = _reflection.GeneratedProtocolMessageType('ListDevicesResponse', (_message.Message,), {
  'DESCRIPTOR' : _LISTDEVICESRESPONSE,
  '__module__' : 'admobilize.devicemanagement.v1alpha1.device_manager_pb2'
  # @@protoc_insertion_point(class_scope:admobilize.devicemanagement.v1alpha1.ListDevicesResponse)
  })
_sym_db.RegisterMessage(ListDevicesResponse)

UpdateDeviceRequest = _reflection.GeneratedProtocolMessageType('UpdateDeviceRequest', (_message.Message,), {
  'DESCRIPTOR' : _UPDATEDEVICEREQUEST,
  '__module__' : 'admobilize.devicemanagement.v1alpha1.device_manager_pb2'
  # @@protoc_insertion_point(class_scope:admobilize.devicemanagement.v1alpha1.UpdateDeviceRequest)
  })
_sym_db.RegisterMessage(UpdateDeviceRequest)

DeleteDeviceRequest = _reflection.GeneratedProtocolMessageType('DeleteDeviceRequest', (_message.Message,), {
  'DESCRIPTOR' : _DELETEDEVICEREQUEST,
  '__module__' : 'admobilize.devicemanagement.v1alpha1.device_manager_pb2'
  # @@protoc_insertion_point(class_scope:admobilize.devicemanagement.v1alpha1.DeleteDeviceRequest)
  })
_sym_db.RegisterMessage(DeleteDeviceRequest)

GetProjectRequest = _reflection.GeneratedProtocolMessageType('GetProjectRequest', (_message.Message,), {
  'DESCRIPTOR' : _GETPROJECTREQUEST,
  '__module__' : 'admobilize.devicemanagement.v1alpha1.device_manager_pb2'
  # @@protoc_insertion_point(class_scope:admobilize.devicemanagement.v1alpha1.GetProjectRequest)
  })
_sym_db.RegisterMessage(GetProjectRequest)

ListProjectsRequest = _reflection.GeneratedProtocolMessageType('ListProjectsRequest', (_message.Message,), {
  'DESCRIPTOR' : _LISTPROJECTSREQUEST,
  '__module__' : 'admobilize.devicemanagement.v1alpha1.device_manager_pb2'
  # @@protoc_insertion_point(class_scope:admobilize.devicemanagement.v1alpha1.ListProjectsRequest)
  })
_sym_db.RegisterMessage(ListProjectsRequest)

ListProjectsResponse = _reflection.GeneratedProtocolMessageType('ListProjectsResponse', (_message.Message,), {
  'DESCRIPTOR' : _LISTPROJECTSRESPONSE,
  '__module__' : 'admobilize.devicemanagement.v1alpha1.device_manager_pb2'
  # @@protoc_insertion_point(class_scope:admobilize.devicemanagement.v1alpha1.ListProjectsResponse)
  })
_sym_db.RegisterMessage(ListProjectsResponse)

UpdateProjectRequest = _reflection.GeneratedProtocolMessageType('UpdateProjectRequest', (_message.Message,), {
  'DESCRIPTOR' : _UPDATEPROJECTREQUEST,
  '__module__' : 'admobilize.devicemanagement.v1alpha1.device_manager_pb2'
  # @@protoc_insertion_point(class_scope:admobilize.devicemanagement.v1alpha1.UpdateProjectRequest)
  })
_sym_db.RegisterMessage(UpdateProjectRequest)

DeleteProjectRequest = _reflection.GeneratedProtocolMessageType('DeleteProjectRequest', (_message.Message,), {
  'DESCRIPTOR' : _DELETEPROJECTREQUEST,
  '__module__' : 'admobilize.devicemanagement.v1alpha1.device_manager_pb2'
  # @@protoc_insertion_point(class_scope:admobilize.devicemanagement.v1alpha1.DeleteProjectRequest)
  })
_sym_db.RegisterMessage(DeleteProjectRequest)

BatchCreateDevicesRequest = _reflection.GeneratedProtocolMessageType('BatchCreateDevicesRequest', (_message.Message,), {
  'DESCRIPTOR' : _BATCHCREATEDEVICESREQUEST,
  '__module__' : 'admobilize.devicemanagement.v1alpha1.device_manager_pb2'
  # @@protoc_insertion_point(class_scope:admobilize.devicemanagement.v1alpha1.BatchCreateDevicesRequest)
  })
_sym_db.RegisterMessage(BatchCreateDevicesRequest)

BatchCreateDevicesResponse = _reflection.GeneratedProtocolMessageType('BatchCreateDevicesResponse', (_message.Message,), {
  'DESCRIPTOR' : _BATCHCREATEDEVICESRESPONSE,
  '__module__' : 'admobilize.devicemanagement.v1alpha1.device_manager_pb2'
  # @@protoc_insertion_point(class_scope:admobilize.devicemanagement.v1alpha1.BatchCreateDevicesResponse)
  })
_sym_db.RegisterMessage(BatchCreateDevicesResponse)

ProvisionDevicesRequest = _reflection.GeneratedProtocolMessageType('ProvisionDevicesRequest', (_message.Message,), {
  'DESCRIPTOR' : _PROVISIONDEVICESREQUEST,
  '__module__' : 'admobilize.devicemanagement.v1alpha1.device_manager_pb2'
  # @@protoc_insertion_point(class_scope:admobilize.devicemanagement.v1alpha1.ProvisionDevicesRequest)
  })
_sym_db.RegisterMessage(ProvisionDevicesRequest)

ProvisionDevicesResponse = _reflection.GeneratedProtocolMessageType('ProvisionDevicesResponse', (_message.Message,), {
  'DESCRIPTOR' : _PROVISIONDEVICESRESPONSE,
  '__module__' : 'admobilize.devicemanagement.v1alpha1.device_manager_pb2'
  # @@protoc_insertion_point(class_scope:admobilize.devicemanagement.v1alpha1.ProvisionDevicesResponse)
  })
_sym_db.RegisterMessage(ProvisionDevicesResponse)

VerifyDeviceTokenRequest = _reflection.GeneratedProtocolMessageType('VerifyDeviceTokenRequest', (_message.Message,), {
  'DESCRIPTOR' : _VERIFYDEVICETOKENREQUEST,
  '__module__' : 'admobilize.devicemanagement.v1alpha1.device_manager_pb2'
  # @@protoc_insertion_point(class_scope:admobilize.devicemanagement.v1alpha1.VerifyDeviceTokenRequest)
  })
_sym_db.RegisterMessage(VerifyDeviceTokenRequest)


DESCRIPTOR._options = None

_DEVICEMANAGER = _descriptor.ServiceDescriptor(
  name='DeviceManager',
  full_name='admobilize.devicemanagement.v1alpha1.DeviceManager',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=1621,
  serialized_end=2749,
  methods=[
  _descriptor.MethodDescriptor(
    name='CreateDevice',
    full_name='admobilize.devicemanagement.v1alpha1.DeviceManager.CreateDevice',
    index=0,
    containing_service=None,
    input_type=admobilize_dot_devicemanagement_dot_v1alpha1_dot_resources__pb2._DEVICE,
    output_type=admobilize_dot_devicemanagement_dot_v1alpha1_dot_resources__pb2._DEVICE,
    serialized_options=b'\202\323\344\223\002\026\"\021/v1alpha1/devices:\001*',
  ),
  _descriptor.MethodDescriptor(
    name='GetDevice',
    full_name='admobilize.devicemanagement.v1alpha1.DeviceManager.GetDevice',
    index=1,
    containing_service=None,
    input_type=_GETDEVICEREQUEST,
    output_type=admobilize_dot_devicemanagement_dot_v1alpha1_dot_resources__pb2._DEVICE,
    serialized_options=b'\202\323\344\223\002\032\022\030/v1alpha1/{id=devices/*}',
  ),
  _descriptor.MethodDescriptor(
    name='ListDevices',
    full_name='admobilize.devicemanagement.v1alpha1.DeviceManager.ListDevices',
    index=2,
    containing_service=None,
    input_type=_LISTDEVICESREQUEST,
    output_type=_LISTDEVICESRESPONSE,
    serialized_options=b'\202\323\344\223\002\023\022\021/v1alpha1/devices',
  ),
  _descriptor.MethodDescriptor(
    name='UpdateDevice',
    full_name='admobilize.devicemanagement.v1alpha1.DeviceManager.UpdateDevice',
    index=3,
    containing_service=None,
    input_type=_UPDATEDEVICEREQUEST,
    output_type=admobilize_dot_devicemanagement_dot_v1alpha1_dot_resources__pb2._DEVICE,
    serialized_options=b'\202\323\344\223\002)2\037/v1alpha1/{device.id=devices/*}:\006device',
  ),
  _descriptor.MethodDescriptor(
    name='DeleteDevice',
    full_name='admobilize.devicemanagement.v1alpha1.DeviceManager.DeleteDevice',
    index=4,
    containing_service=None,
    input_type=_DELETEDEVICEREQUEST,
    output_type=google_dot_protobuf_dot_empty__pb2._EMPTY,
    serialized_options=b'\202\323\344\223\002\032*\030/v1alpha1/{id=devices/*}',
  ),
  _descriptor.MethodDescriptor(
    name='ProvisionDevices',
    full_name='admobilize.devicemanagement.v1alpha1.DeviceManager.ProvisionDevices',
    index=5,
    containing_service=None,
    input_type=_PROVISIONDEVICESREQUEST,
    output_type=_PROVISIONDEVICESRESPONSE,
    serialized_options=b'\202\323\344\223\002 2\033/v1alpha1/devices/provision:\001*',
  ),
  _descriptor.MethodDescriptor(
    name='VerifyDeviceToken',
    full_name='admobilize.devicemanagement.v1alpha1.DeviceManager.VerifyDeviceToken',
    index=6,
    containing_service=None,
    input_type=_VERIFYDEVICETOKENREQUEST,
    output_type=admobilize_dot_devicemanagement_dot_v1alpha1_dot_resources__pb2._DEVICE,
    serialized_options=b'\202\323\344\223\002\037\022\035/v1alpha1/devicetokens/verify',
  ),
])
_sym_db.RegisterServiceDescriptor(_DEVICEMANAGER)

DESCRIPTOR.services_by_name['DeviceManager'] = _DEVICEMANAGER

# @@protoc_insertion_point(module_scope)
