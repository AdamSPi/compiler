.data
.text
.globl _main

_start:
pushq %rbp
movq %rsp, %rbp
pushq %r12
pushq %r13
pushq %r14
pushq %r15
subq $16, %rsp
jmp _body

_body:
callq _read_int
movq %rax, -8(%rbp)
movq -8(%rbp), %r12
negq %r12
addq $196, %r12
negq %r12
addq %r12, %r12
callq _read_int
movq %rax, %r13
addq %r12, %r13
callq _read_int
movq %r13, %r12
addq %rax, %r12
callq _read_int
movq %rax, %rbx
addq %r13, %rbx
movq %rbx, %r13
negq %r13
callq _read_int
movq %rax, %r15
callq _read_int
movq %rax, %r14
addq %r15, %r14
callq _read_int
movq %rax, %rbx
addq %r14, %rbx
addq %r13, %rbx
movq %rbx, %r13
addq %r12, %r13
movq %r13, %r12
addq $-253, %r12
callq _read_int
addq %rax, %r12
movq $153, %rbx
addq %r12, %rbx
negq %rbx
movq $-106, %r12
addq %r13, %r12
addq %rbx, %r12
callq _read_int
negq %rax
addq $28, %rax
addq %r12, %rax
jmp _end

_end:
addq $16, %rsp
popq %r15
popq %r14
popq %r13
popq %r12
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
