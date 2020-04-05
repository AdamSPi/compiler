.section    __TEXT,__text
.globl _main

_start:
pushq %rbp
movq %rsp, %rbp
subq $272, %rsp
jmp _body

_body:
callq _read_int
movq %rax, -8(%rbp)
movq -8(%rbp), %rax
movq %rax, -16(%rbp)
negq -16(%rbp)
callq _read_int
movq %rax, -24(%rbp)
movq -24(%rbp), %rax
movq %rax, -32(%rbp)
addq $-40, -32(%rbp)
movq -32(%rbp), %rax
movq %rax, -40(%rbp)
movq -16(%rbp), %rax
addq %rax, -40(%rbp)
movq -40(%rbp), %rax
movq %rax, -48(%rbp)
negq -48(%rbp)
callq _read_int
movq %rax, -56(%rbp)
callq _read_int
movq %rax, -64(%rbp)
movq -64(%rbp), %rax
movq %rax, -72(%rbp)
movq -56(%rbp), %rax
addq %rax, -72(%rbp)
movq -72(%rbp), %rax
movq %rax, -80(%rbp)
addq $-59, -80(%rbp)
callq _read_int
movq %rax, -88(%rbp)
movq -80(%rbp), %rax
movq %rax, -96(%rbp)
movq -88(%rbp), %rax
addq %rax, -96(%rbp)
movq -96(%rbp), %rax
movq %rax, -104(%rbp)
addq $-52, -104(%rbp)
movq -104(%rbp), %rax
movq %rax, -112(%rbp)
movq -48(%rbp), %rax
addq %rax, -112(%rbp)
callq _read_int
movq %rax, -120(%rbp)
movq -120(%rbp), %rax
movq %rax, -128(%rbp)
addq $30, -128(%rbp)
movq -128(%rbp), %rax
movq %rax, -136(%rbp)
negq -136(%rbp)
movq -136(%rbp), %rax
movq %rax, -144(%rbp)
addq $101, -144(%rbp)
callq _read_int
movq %rax, -152(%rbp)
movq $-210, -160(%rbp)
movq -152(%rbp), %rax
addq %rax, -160(%rbp)
callq _read_int
movq %rax, -168(%rbp)
movq -168(%rbp), %rax
movq %rax, -176(%rbp)
negq -176(%rbp)
movq -176(%rbp), %rax
movq %rax, -184(%rbp)
movq -160(%rbp), %rax
addq %rax, -184(%rbp)
callq _read_int
movq %rax, -192(%rbp)
movq -192(%rbp), %rax
movq %rax, -200(%rbp)
movq -184(%rbp), %rax
addq %rax, -200(%rbp)
movq -200(%rbp), %rax
movq %rax, -208(%rbp)
negq -208(%rbp)
movq -208(%rbp), %rax
movq %rax, -216(%rbp)
movq -144(%rbp), %rax
addq %rax, -216(%rbp)
movq -216(%rbp), %rax
movq %rax, -224(%rbp)
movq -112(%rbp), %rax
addq %rax, -224(%rbp)
callq _read_int
movq %rax, -232(%rbp)
movq -232(%rbp), %rax
movq %rax, -240(%rbp)
addq $-23, -240(%rbp)
movq -224(%rbp), %rax
movq %rax, -248(%rbp)
addq $-59, -248(%rbp)
movq -248(%rbp), %rax
movq %rax, -256(%rbp)
movq -240(%rbp), %rax
addq %rax, -256(%rbp)
movq -256(%rbp), %rax
movq %rax, -264(%rbp)
negq -264(%rbp)
movq -264(%rbp), %rax
movq %rax, -272(%rbp)
negq -272(%rbp)
movq -272(%rbp), %rax
jmp _end

_end:
addq $272, %rsp
popq %rbp
retq

_main:
pushq %rbp
movq %rsp, %rbp
callq _start
movq %rax, %rdi
callq _print_int
popq %rbp
retq
