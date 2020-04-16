.data
.text
.globl main

start:
pushq %rbp
movq %rsp, %rbp
subq $64, %rsp
jmp body

body:
callq read_int
movq %rax, -8(%rbp)
movq -8(%rbp), %rax
movq %rax, -16(%rbp)
negq -16(%rbp)
movq -16(%rbp), %rax
movq %rax, -24(%rbp)
negq -24(%rbp)
movq -24(%rbp), %rax
movq %rax, -32(%rbp)
negq -32(%rbp)
callq read_int
movq %rax, -40(%rbp)
movq $-255, -48(%rbp)
movq -40(%rbp), %rax
addq %rax, -48(%rbp)
movq -48(%rbp), %rax
movq %rax, -56(%rbp)
movq -32(%rbp), %rax
addq %rax, -56(%rbp)
movq -56(%rbp), %rax
movq %rax, -64(%rbp)
negq -64(%rbp)
movq -64(%rbp), %rax
jmp end

end:
addq $64, %rsp
popq %rbp
retq

main:
pushq %rbp
movq %rsp, %rbp
callq start
movq %rax, %rdi
callq print_int
popq %rbp
retq
