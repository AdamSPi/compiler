.data
.text
.globl main

start:
pushq %rbp
movq %rsp, %rbp
subq $160, %rsp
jmp body

body:
callq read_int
movq %rax, -8(%rbp)
movq $-43, -16(%rbp)
movq -8(%rbp), %rax
addq %rax, -16(%rbp)
callq read_int
movq %rax, -24(%rbp)
movq -24(%rbp), %rax
movq %rax, -32(%rbp)
movq -16(%rbp), %rax
addq %rax, -32(%rbp)
callq read_int
movq %rax, -40(%rbp)
callq read_int
movq %rax, -48(%rbp)
movq -48(%rbp), %rax
movq %rax, -56(%rbp)
movq -40(%rbp), %rax
addq %rax, -56(%rbp)
movq -56(%rbp), %rax
movq %rax, -64(%rbp)
addq $-141, -64(%rbp)
movq -64(%rbp), %rax
movq %rax, -72(%rbp)
addq $379, -72(%rbp)
movq -72(%rbp), %rax
movq %rax, -80(%rbp)
movq -32(%rbp), %rax
addq %rax, -80(%rbp)
movq -80(%rbp), %rax
movq %rax, -88(%rbp)
negq -88(%rbp)
callq read_int
movq %rax, -96(%rbp)
movq -96(%rbp), %rax
movq %rax, -104(%rbp)
addq $-281, -104(%rbp)
movq -104(%rbp), %rax
movq %rax, -112(%rbp)
negq -112(%rbp)
callq read_int
movq %rax, -120(%rbp)
movq -120(%rbp), %rax
movq %rax, -128(%rbp)
negq -128(%rbp)
movq -128(%rbp), %rax
movq %rax, -136(%rbp)
movq -88(%rbp), %rax
addq %rax, -136(%rbp)
movq -136(%rbp), %rax
movq %rax, -144(%rbp)
movq -112(%rbp), %rax
addq %rax, -144(%rbp)
callq read_int
movq %rax, -152(%rbp)
movq -152(%rbp), %rax
movq %rax, -160(%rbp)
movq -144(%rbp), %rax
addq %rax, -160(%rbp)
movq -160(%rbp), %rax
jmp end

end:
addq $160, %rsp
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
