.data
.text
.globl main

start:
pushq %rbp
movq %rsp, %rbp
subq $256, %rsp
jmp body

body:
callq read_int
movq %rax, -8(%rbp)
movq -8(%rbp), %rax
movq %rax, -16(%rbp)
negq -16(%rbp)
movq -16(%rbp), %rax
movq %rax, -24(%rbp)
addq $-78, -24(%rbp)
callq read_int
movq %rax, -32(%rbp)
callq read_int
movq %rax, -40(%rbp)
movq -40(%rbp), %rax
movq %rax, -48(%rbp)
movq -32(%rbp), %rax
addq %rax, -48(%rbp)
callq read_int
movq %rax, -56(%rbp)
movq -56(%rbp), %rax
movq %rax, -64(%rbp)
movq -48(%rbp), %rax
addq %rax, -64(%rbp)
callq read_int
movq %rax, -72(%rbp)
movq $-76, -80(%rbp)
movq -72(%rbp), %rax
addq %rax, -80(%rbp)
callq read_int
movq %rax, -88(%rbp)
movq -88(%rbp), %rax
movq %rax, -96(%rbp)
movq -80(%rbp), %rax
addq %rax, -96(%rbp)
movq -96(%rbp), %rax
movq %rax, -104(%rbp)
movq -64(%rbp), %rax
addq %rax, -104(%rbp)
movq -104(%rbp), %rax
movq %rax, -112(%rbp)
movq -24(%rbp), %rax
addq %rax, -112(%rbp)
callq read_int
movq %rax, -120(%rbp)
movq -120(%rbp), %rax
movq %rax, -128(%rbp)
addq $-103, -128(%rbp)
callq read_int
movq %rax, -136(%rbp)
movq -136(%rbp), %rax
movq %rax, -144(%rbp)
negq -144(%rbp)
movq -144(%rbp), %rax
movq %rax, -152(%rbp)
movq -128(%rbp), %rax
addq %rax, -152(%rbp)
movq -152(%rbp), %rax
movq %rax, -160(%rbp)
negq -160(%rbp)
movq -160(%rbp), %rax
movq %rax, -168(%rbp)
movq -160(%rbp), %rax
addq %rax, -168(%rbp)
movq -160(%rbp), %rax
movq %rax, -176(%rbp)
movq -168(%rbp), %rax
addq %rax, -176(%rbp)
movq -160(%rbp), %rax
movq %rax, -184(%rbp)
movq -160(%rbp), %rax
addq %rax, -184(%rbp)
movq -160(%rbp), %rax
movq %rax, -192(%rbp)
addq $-68, -192(%rbp)
movq -192(%rbp), %rax
movq %rax, -200(%rbp)
movq -184(%rbp), %rax
addq %rax, -200(%rbp)
movq -160(%rbp), %rax
movq %rax, -208(%rbp)
negq -208(%rbp)
movq -208(%rbp), %rax
movq %rax, -216(%rbp)
negq -216(%rbp)
movq -216(%rbp), %rax
movq %rax, -224(%rbp)
movq -200(%rbp), %rax
addq %rax, -224(%rbp)
movq -224(%rbp), %rax
movq %rax, -232(%rbp)
negq -232(%rbp)
movq -232(%rbp), %rax
movq %rax, -240(%rbp)
movq -176(%rbp), %rax
addq %rax, -240(%rbp)
movq -240(%rbp), %rax
movq %rax, -248(%rbp)
movq -112(%rbp), %rax
addq %rax, -248(%rbp)
movq -248(%rbp), %rax
jmp end

end:
addq $256, %rsp
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
