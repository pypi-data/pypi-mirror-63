#Settings configured in pillar will override default settings specified in map.jinja
ash-windows:
  lookup:
    apply_lgpo_source: https://watchmaker.cloudarmor.io/repo/microsoft/lgpo/Apply_LGPO_Delta.exe
    apply_lgpo_source_hash: https://watchmaker.cloudarmor.io/repo/microsoft/lgpo/Apply_LGPO_Delta.exe.SHA512
    apply_lgpo_filename: C:\Windows\System32\Apply_LGPO_Delta.exe
    # logdir: C:\Ash\logs
    # role: MemberServer
    # custom_policies:
    #  - policy_type: regpol
    #    key: HKLM\Software\Salt\Foo
    #    value: 1
    #    vtype: REG_DWORD
    #  - policy_type: regpol
    #    key: HKLM\Software\Salt\Bar
    #    value: testing
    #    vtype: REG_SZ
    #  - policy_type: secedit
    #    name: NewAdministratorName
    #    value: superadmin
