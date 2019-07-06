section .data
data_FFFFF8800589E540    dd    31,28,31,30,31,30,31,31,30,31,30,31
data_FFFFF8800589E570    dd    31,29,31,30,31,30,31,31,30,31,30,31
data_FFFFF880058A81F0    db    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
data_FFFFF880058A3170    db    "RtlInitString",0
data_FFFFF8800584C2B7    db    "return",0
data_FFFFF8800584C230    db    "?,biz,net,info,mobi,us,name,me",0
data_FFFFF880058A8238    db    "bcdfghjklmnpqrstvwxyz",0
data_FFFFF880058A8240    db    "aeiou",0
data_FFFFF880058A3010    db    "ExAllocatePool",0
data_FFFFF880058A3018    db    "ExFreePool",0
data_FFFFF880058A2228    db    233
data_FFFFF880058A222D    db    36
data_FFFFF880058A222E    db    0
data_FFFFF880058A2245    db    230
data_FFFFF880058A2246    db    0
data_FFFFF880058A8230    dq    0
data_FFFFF880058A226C    db    10
data_FFFFF880058A2230    db    "?",0
data_FFFFF880058A2248    db    "?",0
data_FFFFF880058A226D    db    "?",0
section .text
global _start
_addr_FFFFF880058523BD:
    MOV QWORD [rsp + 8], rbx
    MOV QWORD [rsp + 16], rbp
    MOV QWORD [rsp + 24], rsi
    MOV QWORD [rsp + 32], rdi
    MOV DWORD r9d, edx
    MOV DWORD eax, 715827883
    IMUL DWORD edx
    SAR DWORD edx, 1
    MOV DWORD eax, edx
    SHR DWORD eax, 31
    ADD DWORD edx, eax
    MOV r10, rcx
    ADD QWORD r10, rdx
    MOV rax, 4294967284
    IMUL DWORD edx
    MOV DWORD edx, eax
    ADD DWORD r9d, edx
    JNS _addr_FFFFF88005892430
    ADD DWORD r9d, 12
    DEC DWORD r10d
    JMP _addr_FFFFF88005892430
_addr_FFFFF88005852C11:
    MOV [rsp-1000], r15
    MOV r15, rax
    SHL QWORD r15, 1
    ADD QWORD r15, rax
    MOV rax, r15
    MOV r15, [rsp-1000]
    MOV rcx, rax
    SHL QWORD rcx, 2
    ADD QWORD rcx, r11
    SHL QWORD rcx, 2
    CMP DWORD ebx, [rcx + rbp]
    JL _addr_FFFFF8800586BD2A
    AND DWORD r8d, r8d
    JNZ _addr_FFFFF880058749EF
    MOV DWORD eax, 1374389535
    MOV rdx, r9
    IMUL DWORD r9d
    SAR DWORD edx, 5
    MOV DWORD eax, edx
    SHR DWORD eax, 31
    ADD DWORD edx, eax
    MOV rax, 100
    IMUL DWORD edx
    MOV DWORD edx, eax
    CMP DWORD r9d, edx
    JNZ _addr_FFFFF8800585E123
    MOV DWORD eax, 1374389535
    MOV rdx, r9
    IMUL DWORD r9d
    SAR DWORD edx, 7
    MOV DWORD eax, edx
    SHR DWORD eax, 31
    ADD DWORD edx, eax
    MOV rax, 400
    IMUL DWORD edx
    MOV DWORD edx, eax
    CMP DWORD r9d, edx
    JNZ _addr_FFFFF880058749EF
    JMP _addr_FFFFF8800585E123
_addr_FFFFF88005853361:
    MOV [rsp-1000], r15
    MOV r15, rax
    SHL QWORD r15, 1
    ADD QWORD r15, rax
    MOV rax, r15
    MOV r15, [rsp-1000]
    MOV rcx, rax
    SHL QWORD rcx, 2
    ADD QWORD rcx, r11
    INC QWORD r11
    SHL QWORD rcx, 2
    SUB DWORD ebx, [rcx + rbp]
    CMP QWORD r11, 12
    JNZ _addr_FFFFF8800586C3D7
    XOR DWORD r11d, r11d
    INC DWORD r10d
    INC DWORD r9d
    JMP _addr_FFFFF8800586C3D7
_addr_FFFFF88005858130:
    MOV DWORD eax, 1374389535
    MOV rdx, r9
    IMUL DWORD r9d
    XOR DWORD r9d, r9d
    SAR DWORD edx, 7
    MOV DWORD eax, edx
    SHR DWORD eax, 31
    ADD DWORD edx, eax
    ADD DWORD edx, ecx
    ADD DWORD edi, edx
    XOR DWORD edx, edx
    AND QWORD r11, r11
    JLE _addr_FFFFF8800588EF92
    JMP _addr_FFFFF880058789EA
_addr_FFFFF8800585BEC8:
    XOR DWORD eax, eax
    JMP _addr_FFFFF8800586C1BA
_addr_FFFFF8800585E123:
    MOV DWORD eax, 1
    JMP _addr_FFFFF88005853361
_addr_FFFFF88005867CB8:
    MOV DWORD eax, 1
    JMP _addr_FFFFF88005852C11
_addr_FFFFF8800586BD2A:
    MOV r9, r10
    ADD QWORD r9, -1970
    MOV DWORD r8d, r10d
    MOV rsi, rbx
    ADD QWORD rsi, 1
    MOV DWORD edi, r9d
    MOV rdx, rdi
    MOV rax, 365
    IMUL DWORD edi
    MOV DWORD edi, eax
    AND DWORD r8d, -2147483645
    JGE _addr_FFFFF8800587D249
    DEC DWORD r8d
    OR DWORD r8d, -4
    INC DWORD r8d
    JMP _addr_FFFFF8800587D249
_addr_FFFFF8800586C1BA:
    MOV [rsp-1000], r15
    MOV r15, rax
    SHL QWORD r15, 1
    ADD QWORD r15, rax
    MOV rax, r15
    MOV r15, [rsp-1000]
    MOV rcx, rax
    SHL QWORD rcx, 2
    ADD QWORD rcx, r11
    SHL QWORD rcx, 2
    ADD DWORD ebx, [rcx + rbp]
    JS _addr_FFFFF88005879356
    JMP _addr_FFFFF8800587D806
_addr_FFFFF8800586C3D7:
    MOV DWORD r8d, r9d
    AND DWORD r8d, -2147483645
    JGE _addr_FFFFF880058766F6
    DEC DWORD r8d
    OR DWORD r8d, -4
    INC DWORD r8d
    JMP _addr_FFFFF880058766F6
_addr_FFFFF8800586DCDA:
    MOV DWORD eax, 1
    JMP _addr_FFFFF8800586C1BA
_addr_FFFFF88005871617:
    MOV DWORD eax, r8d
    AND DWORD eax, -2147483645
    JGE _addr_FFFFF8800588573A
    DEC DWORD eax
    OR DWORD eax, -4
    INC DWORD eax
    JMP _addr_FFFFF8800588573A
_addr_FFFFF880058749EF:
    XOR DWORD eax, eax
    JMP _addr_FFFFF88005853361
_addr_FFFFF880058766F6:
    AND DWORD r8d, r8d
    JNZ _addr_FFFFF8800587C8F8
    MOV DWORD eax, 1374389535
    MOV rdx, r9
    IMUL DWORD r9d
    SAR DWORD edx, 5
    MOV DWORD eax, edx
    SHR DWORD eax, 31
    ADD DWORD edx, eax
    MOV rax, 100
    IMUL DWORD edx
    MOV DWORD edx, eax
    CMP DWORD r9d, edx
    JNZ _addr_FFFFF88005867CB8
    MOV DWORD eax, 1374389535
    MOV rdx, r9
    IMUL DWORD r9d
    SAR DWORD edx, 7
    MOV DWORD eax, edx
    SHR DWORD eax, 31
    ADD DWORD edx, eax
    MOV rax, 400
    IMUL DWORD edx
    MOV DWORD edx, eax
    CMP DWORD r9d, edx
    JNZ _addr_FFFFF8800587C8F8
    JMP _addr_FFFFF88005867CB8
_addr_FFFFF880058789EA:
    AND DWORD r8d, r8d
    JNZ _addr_FFFFF8800588A61B
    AND DWORD ebx, ebx
    JNZ _addr_FFFFF8800588FCBA
    AND DWORD r10d, r10d
    JNZ _addr_FFFFF8800588A61B
    JMP _addr_FFFFF8800588FCBA
_addr_FFFFF88005879356:
    DEC DWORD r9d
    DEC QWORD r11
    JNS _addr_FFFFF88005871617
    MOV DWORD r9d, 11
    DEC DWORD r10d
    DEC DWORD r8d
    MOV DWORD r11d, r9d
    JMP _addr_FFFFF88005871617
_addr_FFFFF8800587C8F8:
    XOR DWORD eax, eax
    JMP _addr_FFFFF88005852C11
_addr_FFFFF8800587D249:
    AND DWORD r8d, r8d
    JZ _addr_FFFFF8800588D196
    CMP DWORD r8d, 2
    JGE _addr_FFFFF8800588D196
    MOV DWORD ecx, 1
    JMP _addr_FFFFF88005898139
_addr_FFFFF8800587D806:
    MOV QWORD r11, r9
    MOV r9, r10
    ADD QWORD r9, 1900
    JMP _addr_FFFFF8800586C3D7
_addr_FFFFF8800587FC5A:
    XOR DWORD ecx, ecx
    JMP _addr_FFFFF88005858130
_addr_FFFFF8800588573A:
    AND DWORD eax, eax
    JNZ _addr_FFFFF8800585BEC8
    MOV DWORD eax, 1374389535
    MOV rdx, r8
    IMUL DWORD r8d
    SAR DWORD edx, 5
    MOV DWORD eax, edx
    SHR DWORD eax, 31
    ADD DWORD edx, eax
    MOV rax, 100
    IMUL DWORD edx
    MOV DWORD edx, eax
    CMP DWORD r8d, edx
    JNZ _addr_FFFFF8800586DCDA
    MOV DWORD eax, 1374389535
    MOV rdx, r8
    IMUL DWORD r8d
    SAR DWORD edx, 7
    MOV DWORD eax, edx
    SHR DWORD eax, 31
    ADD DWORD edx, eax
    MOV rax, 400
    IMUL DWORD edx
    MOV DWORD edx, eax
    CMP DWORD r8d, edx
    JNZ _addr_FFFFF8800585BEC8
    JMP _addr_FFFFF8800586DCDA
_addr_FFFFF88005888F56:
    NEG DWORD ecx
    MOV DWORD eax, 1374389535
    MOV rdx, r9
    IMUL DWORD r9d
    SAR DWORD edx, 5
    MOV DWORD eax, edx
    SHR DWORD eax, 31
    ADD DWORD edx, eax
    MOV DWORD eax, 1374389535
    SUB DWORD ecx, edx
    ADD DWORD edi, ecx
    MOV rdx, r10
    IMUL DWORD r10d
    SAR DWORD edx, 7
    MOV DWORD eax, edx
    SHR DWORD eax, 31
    ADD DWORD edx, eax
    MOV rax, 400
    IMUL DWORD edx
    MOV DWORD edx, eax
    SUB DWORD r10d, edx
    JZ _addr_FFFFF8800587FC5A
    CMP DWORD r10d, 370
    JGE _addr_FFFFF8800587FC5A
    MOV DWORD ecx, 1
    JMP _addr_FFFFF88005858130
_addr_FFFFF8800588A61B:
    XOR DWORD eax, eax
    JMP _addr_FFFFF88005898022
_addr_FFFFF8800588D196:
    XOR DWORD ecx, ecx
    JMP _addr_FFFFF88005898139
_addr_FFFFF8800588EF92:
    MOV QWORD rbx, [rsp + 8]
    MOV QWORD rbp, [rsp + 16]
    MOV rax, rdi
    ADD QWORD rax, r9
    MOV QWORD rdi, [rsp + 32]
    MOV [rsp-1000], r15
    MOV r15, rsi
    ADD QWORD r15, rax
    ADD QWORD r15, -1
    MOV DWORD eax, esi
    MOV rax, r15
    MOV r15, [rsp-1000]
    MOV QWORD rsi, [rsp + 24]
    ADD QWORD rsp, 8
    RET
_addr_FFFFF8800588FCBA:
    MOV DWORD eax, 1
    JMP _addr_FFFFF88005898022
_addr_FFFFF88005892430:
    MOV rbx, r8
    ADD QWORD rbx, -1
    MOV QWORD r11, r9
    MOV QWORD rbp, data_FFFFF8800589E540
    AND DWORD ebx, ebx
    JNS _addr_FFFFF8800587D806
    MOV r8, r10
    ADD QWORD r8, 1900
    JMP _addr_FFFFF88005879356
_addr_FFFFF88005898022:
    MOV [rsp-1000], r15
    MOV r15, rax
    SHL QWORD r15, 1
    ADD QWORD r15, rax
    MOV rax, r15
    MOV r15, [rsp-1000]
    MOV rcx, rax
    SHL QWORD rcx, 2
    ADD QWORD rcx, rdx
    INC QWORD rdx
    SHL QWORD rcx, 2
    ADD DWORD r9d, [rcx + rbp]
    CMP QWORD rdx, r11
    JL _addr_FFFFF880058789EA
    JMP _addr_FFFFF8800588EF92
_addr_FFFFF88005898139:
    MOV DWORD eax, r9d
    MOV DWORD ebx, r10d
    CDQ
    AND DWORD edx, 3
    ADD DWORD eax, edx
    SAR DWORD eax, 2
    ADD DWORD eax, ecx
    ADD DWORD edi, eax
    MOV DWORD eax, 1374389535
    MOV rdx, r10
    IMUL DWORD r10d
    SAR DWORD edx, 5
    MOV DWORD eax, edx
    SHR DWORD eax, 31
    ADD DWORD edx, eax
    MOV rax, 100
    IMUL DWORD edx
    MOV DWORD edx, eax
    SUB DWORD ebx, edx
    JZ _addr_FFFFF8800589C790
    CMP DWORD ebx, 70
    JGE _addr_FFFFF8800589C790
    MOV DWORD ecx, 1
    JMP _addr_FFFFF88005888F56
_addr_FFFFF8800589C790:
    XOR DWORD ecx, ecx
    JMP _addr_FFFFF88005888F56
_addr_FFFFF88005851A83:
    MOV DWORD eax, [rcx]
    INC QWORD rcx
    MOV BYTE [rsi + rcx], al
    AND BYTE al, al
    JNZ _addr_FFFFF88005851A83
    MOV QWORD rbx, [rsp + 296]
    ADD QWORD rsp, 224
    ADD QWORD rsp, 8
    MOV QWORD r15, [rsp]
    ADD QWORD rsp, 8
    MOV QWORD r14, [rsp]
    ADD QWORD rsp, 8
    MOV QWORD r13, [rsp]
    ADD QWORD rsp, 8
    MOV QWORD r12, [rsp]
    ADD QWORD rsp, 8
    MOV QWORD rdi, [rsp]
    ADD QWORD rsp, 8
    MOV QWORD rsi, [rsp]
    ADD QWORD rsp, 8
    MOV QWORD rbp, [rsp]
    ADD QWORD rsp, 8
    RET
_addr_FFFFF880058549F2:
    CMP QWORD r10, r11
    JB _addr_FFFFF8800588B329
    MOV QWORD r9, [data_FFFFF880058A8230]
    JMP _addr_FFFFF88005879426
_addr_FFFFF88005857A96:
    MOV QWORD r13, [data_FFFFF880058A8240]
    AND QWORD r13, r13
    JNZ _addr_FFFFF8800586C445
    MOV rdx, r13
    ADD QWORD rdx, 7
    XOR DWORD ecx, ecx
    CALL [data_FFFFF880058A3010]
    CMP BYTE [data_FFFFF880058A222D], bl
    MOV QWORD r13, rax
    MOV QWORD [data_FFFFF880058A8240], rax
    JZ _addr_FFFFF8800586C445
    MOV DWORD [rsp + 32], -967459448
    MOV DWORD r8d, ebx
    MOV QWORD r9, data_FFFFF880058A2228
    MOV QWORD r10, data_FFFFF880058A222E
    JMP _addr_FFFFF8800588F707
_addr_FFFFF8800585A771:
    MOV DWORD ecx, r8d
    MOV DWORD eax, edi
    MOV DWORD edx, r11d
    SHR BYTE dl, cl
    MOV DWORD ecx, r8d
    INC DWORD r12d
    SHL BYTE al, cl
    XOR BYTE dl, al
    MOV QWORD rax, r8
    MOV DWORD r8d, [rbp + 127]
    MOV DWORD eax, [rsp + rax + 40]
    SHR BYTE al, 4
    IMUL BYTE dl
    MOV DWORD ecx, eax
    MOV rax, r8
    ADD QWORD rax, 1
    MOV rdx, rcx
    IMUL BYTE cl
    INC QWORD r9
    MOV BYTE [r9 + -1], al
    JMP _addr_FFFFF880058806A0
_addr_FFFFF8800585C674:
    MOV rax, rbp
    ADD QWORD rax, -113
    MOV DWORD edx, 1
    MOV QWORD [rbp + -49], rax
    CMP BYTE [rbp + -113], bl
    JZ _addr_FFFFF88005884B91
    JMP _addr_FFFFF880058645F0
_addr_FFFFF8800585D92A:
    CMP DWORD ebx, r10d
    JL _addr_FFFFF88005882B20
    JMP _addr_FFFFF88005884F8C
_addr_FFFFF880058645F0:
    CMP BYTE [rdi], 44
    JNZ _addr_FFFFF88005883B92
    MOV QWORD rax, rdx
    MOV rcx, rdi
    ADD QWORD rcx, 1
    MOV BYTE [rdi], bl
    SHL QWORD rax, 3
    MOV QWORD [rbp + rax + -49], rcx
    INC DWORD edx
    JMP _addr_FFFFF88005883B92
_addr_FFFFF8800586C445:
    MOV QWORD r9, [data_FFFFF880058A8230]
    AND QWORD r9, r9
    JNZ _addr_FFFFF88005879426
    MOV rdx, r9
    ADD QWORD rdx, 38
    XOR DWORD ecx, ecx
    CALL [data_FFFFF880058A3010]
    CMP BYTE [data_FFFFF880058A226C], bl
    MOV QWORD r9, rax
    MOV QWORD [data_FFFFF880058A8230], rax
    JZ _addr_FFFFF88005879426
    MOV DWORD [rsp + 32], 2131189013
    MOV DWORD r8d, ebx
    MOV QWORD r10, data_FFFFF880058A2248
    MOV QWORD r11, data_FFFFF880058A226D
    JMP _addr_FFFFF8800588B329
_start:
    PUSH rbp
    MOV rbp, rsp
    MOV QWORD [rsp + 16], rbx
    MOV QWORD [rsp + 32], r9
    SUB QWORD rsp, 8
    MOV QWORD [rsp], rbp
    SUB QWORD rsp, 8
    MOV QWORD [rsp], rsi
    SUB QWORD rsp, 8
    MOV QWORD [rsp], rdi
    SUB QWORD rsp, 8
    MOV QWORD [rsp], r12
    SUB QWORD rsp, 8
    MOV QWORD [rsp], r13
    SUB QWORD rsp, 8
    MOV QWORD [rsp], r14
    SUB QWORD rsp, 8
    MOV QWORD [rsp], r15
    MOV rbp, rsp
    ADD QWORD rbp, -31
    SUB QWORD rsp, 224
    XOR DWORD ebx, ebx
    MOV QWORD rsi, r9
    MOV DWORD edi, ecx
    MOV DWORD r12d, ebx
    MOV DWORD [rsp + 40], 229629996
    CALL _addr_FFFFF880058523BD
    MOV QWORD r14, [data_FFFFF880058A8238]
    MOV DWORD r11d, eax
    SUB BYTE dil, 108
    MOV DWORD eax, 1431655766
    MOV DWORD [rbp + 95], edi
    MOV DWORD r15d, ebx
    MOV rdi, rbp
    ADD QWORD rdi, -113
    MOV rdx, [rbp + 127]
    IMUL DWORD [rbp + 127]
    MOV DWORD eax, edx
    ADD DWORD edx, r11d
    SHR DWORD eax, 31
    ADD DWORD eax, edx
    MOV DWORD [rsp + 48], eax
    AND QWORD r14, r14
    JNZ _addr_FFFFF88005857A96
    MOV rdx, rbx
    ADD QWORD rdx, 23
    XOR DWORD ecx, ecx
    CALL [data_FFFFF880058A3010]
    CMP BYTE [data_FFFFF880058A2245], bl
    MOV QWORD r14, rax
    MOV QWORD [data_FFFFF880058A8238], rax
    JZ _addr_FFFFF88005857A96
    MOV DWORD [rsp + 32], 862290972
    MOV DWORD r8d, ebx
    MOV QWORD r9, data_FFFFF880058A2230
    MOV QWORD r10, data_FFFFF880058A2246
    JMP _addr_FFFFF88005898C74
_addr_FFFFF8800586FD9E:
    MOV DWORD r8d, [rbp + 127]
    JMP _addr_FFFFF880058806A0
_addr_FFFFF88005873965:
    CMP QWORD r9, r10
    JB _addr_FFFFF88005898C74
    MOV QWORD r14, [data_FFFFF880058A8238]
    JMP _addr_FFFFF88005857A96
_addr_FFFFF880058745FC:
    INC DWORD ebx
    JMP _addr_FFFFF8800585D92A
_addr_FFFFF88005879426:
    MOV rdx, rbp
    ADD QWORD rdx, -113
    MOV QWORD rcx, r9
    SUB QWORD rdx, r9
    JMP _addr_FFFFF8800589BB68
_addr_FFFFF8800587CD7B:
    MOV QWORD rax, r8
    MOV DWORD ecx, r8d
    MOV DWORD r8d, [rbp + 127]
    MOV DWORD edx, [rsp + rax + 40]
    MOV DWORD eax, esi
    INC DWORD r12d
    SHL BYTE al, cl
    AND BYTE dl, 15
    IMUL BYTE dl
    MOV DWORD ecx, eax
    MOV rax, r8
    ADD QWORD rax, 1
    MOV rdx, rcx
    IMUL BYTE cl
    INC QWORD r9
    MOV BYTE [r9 + -1], al
    JMP _addr_FFFFF880058806A0
_addr_FFFFF880058806A0:
    CMP DWORD r12d, r10d
    JL _addr_FFFFF8800588E6A4
    MOV QWORD rsi, [rbp + 119]
    AND DWORD r10d, r10d
    JLE _addr_FFFFF88005884F8C
    JMP _addr_FFFFF88005882B20
_addr_FFFFF88005882B20:
    MOV QWORD rax, rbx
    INC DWORD ebx
    MOV DWORD ecx, [rsp + rax + 56]
    AND BYTE cl, cl
    JNS _addr_FFFFF88005893DA9
    MOV DWORD eax, 818089009
    INC QWORD rsi
    MOV rdx, rcx
    IMUL DWORD ecx
    SAR DWORD edx, 2
    MOV DWORD eax, edx
    SHR DWORD eax, 31
    ADD DWORD edx, eax
    MOV rax, 21
    IMUL DWORD edx
    MOV DWORD edx, eax
    SUB DWORD ecx, edx
    MOV QWORD rax, rcx
    MOV DWORD ecx, [r14 + rax]
    MOV BYTE [rsi + -1], cl
    CMP DWORD ebx, r10d
    JGE _addr_FFFFF88005884F8C
    MOV QWORD rax, rbx
    INC DWORD ebx
    INC QWORD rsi
    MOV DWORD ecx, [rsp + rax + 56]
    MOV DWORD eax, 1717986919
    MOV rdx, rcx
    IMUL DWORD ecx
    SAR DWORD edx, 1
    MOV DWORD eax, edx
    SHR DWORD eax, 31
    ADD DWORD edx, eax
    MOV rax, rdx
    SHL QWORD rax, 2
    ADD QWORD rax, rdx
    SUB DWORD ecx, eax
    MOV QWORD rax, rcx
    MOV DWORD ecx, [r13 + rax]
    MOV BYTE [rsi + -1], cl
    CMP DWORD ebx, r10d
    JGE _addr_FFFFF88005884F8C
    MOV QWORD rax, rbx
    MOV DWORD ecx, [rsp + rax + 56]
    AND BYTE cl, 64
    JZ _addr_FFFFF8800585D92A
    MOV DWORD eax, 1717986919
    MOV rdx, rcx
    IMUL DWORD ecx
    SAR DWORD edx, 1
    MOV DWORD eax, edx
    SHR DWORD eax, 31
    ADD DWORD edx, eax
    MOV rax, rdx
    SHL QWORD rax, 2
    ADD QWORD rax, rdx
    SUB DWORD ecx, eax
    INC QWORD rsi
    MOV QWORD rax, rcx
    MOV DWORD ecx, [r13 + rax]
    MOV BYTE [rsi + -1], cl
    JMP _addr_FFFFF880058745FC
_addr_FFFFF88005883B92:
    INC QWORD rdi
    CMP BYTE [rdi], bl
    JNZ _addr_FFFFF880058645F0
    JMP _addr_FFFFF88005884B91
_addr_FFFFF88005884B91:
    MOV DWORD r8d, [rbp + 127]
    MOV DWORD eax, -858993459
    MOV DWORD ecx, r8d
    MUL DWORD [rsp + 48]
    SHR DWORD edx, 3
    MOV rax, r8
    ADD QWORD rax, -1
    MOV r11, rdx
    SHL QWORD r11, 2
    ADD QWORD r11, rdx
    MOV DWORD edx, 229629996
    SHR DWORD edx, cl
    ADD DWORD r11d, r11d
    MOV DWORD [rsp + 48], r11d
    IMUL BYTE dl
    MOV DWORD ecx, eax
    MOV DWORD eax, r11d
    MOV rdx, rcx
    IMUL BYTE cl
    AND BYTE al, 1
    ADD BYTE al, 8
    MOV DWORD r10d, eax
    AND DWORD r10d, r10d
    JLE _addr_FFFFF88005884F8C
    MOV DWORD edi, [rsp + 49]
    MOV DWORD esi, [rbp + 95]
    MOV r9, rsp
    ADD QWORD r9, 56
    JMP _addr_FFFFF8800588E6A4
_addr_FFFFF88005884F8C:
    XOR DWORD r11d, r8d
    MOV DWORD eax, 954437177
    MOV BYTE [rsi], 46
    XOR DWORD r11d, 229629996
    MUL DWORD r11d
    SHR DWORD edx, 1
    MOV rax, rdx
    SHL QWORD rax, 3
    ADD QWORD rax, rdx
    SUB DWORD r11d, eax
    MOV rcx, r11
    SHL QWORD rcx, 3
    MOV QWORD rcx, [rbp + r11 + -49]
    SUB QWORD rsi, rcx
    JMP _addr_FFFFF88005851A83
_addr_FFFFF8800588B329:
    MOV QWORD rdx, r8
    INC QWORD r9
    INC QWORD r10
    MOV DWORD ecx, [rsp + rdx + 32]
    MOV DWORD eax, ecx
    XOR BYTE al, [r10 + -1]
    MOV BYTE [r9 + -1], al
    MOV DWORD eax, ecx
    ADD BYTE cl, cl
    SHR BYTE al, 1
    XOR BYTE al, cl
    INC DWORD r8d
    AND DWORD r8d, -2147483645
    MOV BYTE [rsp + rdx + 32], al
    JGE _addr_FFFFF880058549F2
    DEC DWORD r8d
    OR DWORD r8d, -4
    INC DWORD r8d
    JMP _addr_FFFFF880058549F2
_addr_FFFFF8800588E6A4:
    MOV DWORD eax, r15d
    INC DWORD r15d
    CDQ
    AND DWORD edx, 3
    ADD DWORD eax, edx
    MOV DWORD r8d, eax
    AND DWORD eax, 3
    SAR DWORD r8d, 2
    SUB DWORD eax, edx
    JZ _addr_FFFFF88005893D0B
    DEC DWORD eax
    JZ _addr_FFFFF8800587CD7B
    DEC DWORD eax
    JZ _addr_FFFFF8800585A771
    DEC DWORD eax
    JNZ _addr_FFFFF8800586FD9E
    MOV DWORD ecx, r8d
    MOV DWORD eax, r11d
    MOV DWORD edx, edi
    SHR BYTE dl, cl
    MOV DWORD ecx, r8d
    INC DWORD r12d
    SHL BYTE al, cl
    XOR BYTE dl, al
    MOV QWORD rax, r8
    MOV DWORD r8d, [rbp + 127]
    MOV DWORD eax, [rsp + rax + 40]
    AND BYTE al, 15
    IMUL BYTE dl
    MOV DWORD ecx, eax
    MOV rax, r8
    ADD QWORD rax, 1
    MOV rdx, rcx
    IMUL BYTE cl
    INC QWORD r9
    MOV BYTE [r9 + -1], al
    JMP _addr_FFFFF880058806A0
_addr_FFFFF8800588F707:
    MOV QWORD rdx, r8
    INC QWORD r13
    INC QWORD r9
    MOV DWORD ecx, [rsp + rdx + 32]
    MOV DWORD eax, ecx
    XOR BYTE al, [r9 + -1]
    MOV BYTE [r13 + -1], al
    MOV DWORD eax, ecx
    ADD BYTE cl, cl
    SHR BYTE al, 1
    XOR BYTE al, cl
    INC DWORD r8d
    AND DWORD r8d, -2147483645
    MOV BYTE [rsp + rdx + 32], al
    JGE _addr_FFFFF88005891937
    DEC DWORD r8d
    OR DWORD r8d, -4
    INC DWORD r8d
    JMP _addr_FFFFF88005891937
_addr_FFFFF88005891937:
    CMP QWORD r9, r10
    JB _addr_FFFFF8800588F707
    MOV QWORD r13, [data_FFFFF880058A8240]
    JMP _addr_FFFFF8800586C445
_addr_FFFFF88005893D0B:
    MOV QWORD rax, r8
    MOV DWORD ecx, r8d
    MOV DWORD r8d, [rbp + 127]
    MOV DWORD edx, [rsp + rax + 40]
    MOV DWORD eax, esi
    INC DWORD r12d
    SHR BYTE al, cl
    SHR BYTE dl, 4
    IMUL BYTE dl
    MOV DWORD ecx, eax
    MOV rax, r8
    ADD QWORD rax, 1
    MOV rdx, rcx
    IMUL BYTE cl
    INC QWORD r9
    MOV BYTE [r9 + -1], al
    JMP _addr_FFFFF880058806A0
_addr_FFFFF88005893DA9:
    MOV DWORD eax, 1717986919
    MOV rdx, rcx
    IMUL DWORD ecx
    SAR DWORD edx, 1
    MOV DWORD eax, edx
    SHR DWORD eax, 31
    ADD DWORD edx, eax
    MOV rax, rdx
    SHL QWORD rax, 2
    ADD QWORD rax, rdx
    SUB DWORD ecx, eax
    MOV QWORD rax, rcx
    MOV DWORD ecx, [r13 + rax]
    MOV QWORD rax, rbx
    MOV BYTE [rsi], cl
    MOV DWORD ecx, [rsp + rax + 56]
    MOV DWORD eax, 818089009
    MOV rdx, rcx
    IMUL DWORD ecx
    SAR DWORD edx, 2
    MOV DWORD eax, edx
    SHR DWORD eax, 31
    ADD DWORD edx, eax
    MOV rax, 21
    IMUL DWORD edx
    MOV DWORD edx, eax
    SUB DWORD ecx, edx
    ADD QWORD rsi, 2
    MOV QWORD rax, rcx
    MOV DWORD ecx, [r14 + rax]
    MOV BYTE [rsi + -1], cl
    JMP _addr_FFFFF880058745FC
_addr_FFFFF88005898C74:
    MOV QWORD rdx, r8
    INC QWORD r14
    INC QWORD r9
    MOV DWORD ecx, [rsp + rdx + 32]
    MOV DWORD eax, ecx
    XOR BYTE al, [r9 + -1]
    MOV BYTE [r14 + -1], al
    MOV DWORD eax, ecx
    ADD BYTE cl, cl
    SHR BYTE al, 1
    XOR BYTE al, cl
    INC DWORD r8d
    AND DWORD r8d, -2147483645
    MOV BYTE [rsp + rdx + 32], al
    JGE _addr_FFFFF88005873965
    DEC DWORD r8d
    OR DWORD r8d, -4
    INC DWORD r8d
    JMP _addr_FFFFF88005873965
_addr_FFFFF8800589BB68:
    MOV DWORD eax, [rcx]
    INC QWORD rcx
    MOV BYTE [rdx + rcx + -1], al
    AND BYTE al, al
    JNZ _addr_FFFFF8800589BB68
    AND QWORD r9, r9
    JZ _addr_FFFFF8800585C674
    MOV QWORD rcx, r9
    CALL [data_FFFFF880058A3018]
    MOV QWORD [data_FFFFF880058A8230], rbx
    JMP _addr_FFFFF8800585C674
