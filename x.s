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
subq $0, %rsp
jmp _body

_body:
callq _read_int
movq %rax, %r12
callq _read_int
movq %rax, %r14
negq %r14
addq %r14, %r14
addq $-357, %r14
callq _read_int
movq %rax, %r13
negq %r13
callq _read_int
movq %rax, %rbx
addq %r14, %rbx
addq %r13, %rbx
movq $149, %rcx
addq %rbx, %rcx
movq %rcx, %rbx
negq %rbx
addq %r12, %rbx
movq %rbx, %r12
negq %r12
callq _read_int
movq %rax, %r13
callq _read_int
movq %rax, %r14
negq %r14
addq %r13, %r14
callq _read_int
movq %rax, %r13
addq $137, %r13
addq %r14, %r13
callq _read_int
movq %rax, %r15
addq $-405, %r15
callq _read_int
movq %rax, %r14
addq %r15, %r14
callq _read_int
movq %rax, %rbx
negq %rbx
movq %r14, %rax
addq $-235, %rax
addq %rbx, %rax
movq %r14, %rbx
addq %r14, %rbx
addq %rax, %rbx
addq %r13, %rbx
addq %r12, %rbx
movq %rbx, %rax
jmp _end

_end:
addq $0, %rsp
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
