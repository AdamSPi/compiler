.data
.text
.globl _main

_start:
pushq %rbp
movq %rsp, %rbp
subq $64, %rsp
jmp _body

_body:
callq _read_int
movq %rax, %r12
callq _read_int
movq %rax, %rbx
callq _read_int
movq %rax, -8(%rbp)
movq -8(%rbp), %rdx
addq %rbx, %rdx
movq %rdx, %rbx
addq %r12, %rbx
callq _read_int
movq %rax, -16(%rbp)
movq %rbx, %rdx
addq -16(%rbp), %rdx
movq $166, %r12
addq %rdx, %r12
callq _read_int
movq %rax, -24(%rbp)
movq -24(%rbp), %rdx
addq %r12, %rdx
movq %rdx, %r12
negq %r12
callq _read_int
movq %rax, -32(%rbp)
movq -32(%rbp), %r13
negq %r13
callq _read_int
movq %rax, %r14
callq _read_int
movq %rax, -40(%rbp)
movq -40(%rbp), %rdx
addq %r14, %rdx
movq %rdx, %rdx
addq %r13, %rdx
movq %r12, %rcx
addq %rbx, %rcx
movq %rcx, %rbx
addq $-70, %rbx
movq %rbx, %rbx
addq %rdx, %rbx
callq _read_int
movq %rax, %rdx
movq $-384, -48(%rbp)
addq %rdx, -48(%rbp)
movq %rbx, %rbx
negq %rbx
movq %rbx, %rbx
addq -48(%rbp), %rbx
movq %rbx, -56(%rbp)
addq $171, -56(%rbp)
movq -56(%rbp), %rax
jmp _end

_end:
addq $64, %rsp
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
