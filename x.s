.data
.text
.globl main

start:
pushq %rbp
movq %rsp, %rbp
subq $80, %rsp
jmp body

body:
callq read_int
movq %rax, -8(%rbp)
callq read_int
movq %rax, -16(%rbp)
movq -16(%rbp), %rax
movq %rax, -24(%rbp)
movq -8(%rbp), %rax
addq %rax, -24(%rbp)
movq $-106, -32(%rbp)
movq -24(%rbp), %rax
addq %rax, -32(%rbp)
movq -32(%rbp), %rax
movq %rax, -40(%rbp)
negq -40(%rbp)
movq -40(%rbp), %rax
movq %rax, -48(%rbp)
movq -24(%rbp), %rax
addq %rax, -48(%rbp)
movq -48(%rbp), %rax
movq %rax, -56(%rbp)
movq -24(%rbp), %rax
addq %rax, -56(%rbp)
movq -56(%rbp), %rax
movq %rax, -64(%rbp)
addq $54, -64(%rbp)
movq -64(%rbp), %rax
movq %rax, -72(%rbp)
negq -72(%rbp)
movq -72(%rbp), %rax
jmp end

end:
addq $80, %rsp
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
