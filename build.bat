@echo off
chcp 65001 > nul
set "MSVC=D:\NewSutdy\development\visual studio\community\VC\Tools\MSVC\14.50.35717"
set "SDK=D:\Windows Kits\10"
set "EASYX=D:\Google DownLoad\EasyX_26.1.1 (1)"
set "PATH=%MSVC%\bin\Hostx64\x64;%PATH%"
set "INCLUDE=%MSVC%\include;%SDK%\Include\10.0.26100.0\ucrt;%SDK%\Include\10.0.26100.0\shared;%SDK%\Include\10.0.26100.0\um;%EASYX%\include"
set "LIB=%MSVC%\lib\x64;%SDK%\Lib\10.0.26100.0\um\x64;%SDK%\Lib\10.0.26100.0\ucrt\x64;%EASYX%\lib\VC2015\x64"

cd /d "D:\1\0252852\plane_war"
echo ===== MBCS build =====
cl /nologo /EHsc /MD main.cpp /Fe:main.exe /link user32.lib gdi32.lib shell32.lib 2>&1
if %ERRORLEVEL% NEQ 0 (echo MBCS FAILED && exit /b 1)

echo ===== Unicode build =====
cl /nologo /EHsc /MD /DUNICODE /D_UNICODE main.cpp /Fe:main_u.exe /link user32.lib gdi32.lib shell32.lib 2>&1
if %ERRORLEVEL% NEQ 0 (echo UNICODE FAILED && exit /b 1)

echo ===== BOTH OK ====
