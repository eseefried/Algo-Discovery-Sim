OPENQASM 2.0;
include "qelib1.inc";
qreg q[2];
u(0,0,0.65) q[0];
u(0,0,1.85) q[1];
cx q[0],q[1];
u(0,0,0.04999999999999993) q[1];
cx q[0],q[1];
