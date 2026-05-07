; Script tạo bộ cài cho BP Auto Gach No
#define MyAppName "BP Auto Gach No"
#define MyAppVersion "1.1.2"
#define MyAppPublisher "CMTHANG"
#define MyAppExeName "BPAutoGachNo.exe"
#define MyAppIconName "Logo512.ico"

[Setup]
AppId={{D3F9E2B2-7C1D-4A5F-9B6D-8E1A3C4B5D6E}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
; Cho phép người dùng chọn thư mục cài đặt
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
; Tạo file Setup_v1.1.2.exe
OutputBaseFilename=BPAutoGachNo_Setup_v1.1.2
SetupIconFile={#MyAppIconName}
Compression=lzma
SolidCompression=yes
WizardStyle=modern
; Hiển thị trong Add/Remove Programs
UninstallDisplayIcon={app}\{#MyAppExeName}

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
; Lấy toàn bộ thư mục đã build từ PyInstaller bao gồm cả pw-browser
Source: "dist\BPAutoGachNo\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "Logo512.ico"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\{#MyAppIconName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\{#MyAppIconName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent
