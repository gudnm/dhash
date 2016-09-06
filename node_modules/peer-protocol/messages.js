var protobuf = require('protocol-buffers')

module.exports = protobuf(`message Open {
  required bytes key = 1;
  required bytes nonce = 2;
}

message Handshake {
  required bytes id = 1;
  repeated string extensions = 2;
}`)
