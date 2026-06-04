@echo off
chcp 65001 > nul
set "MSVC=D:\NewSutdy\development\visual studio\community\VC\Tools\MSVC\14.50.35717"
set "SDK=D:\Windows Kits\10"
set "EASYX=D:\Google DownLoad\EasyX_26.1.1 (1)"
set "PATH=%MSVC%\bin\Hostx64\x64;%PATH%"
set "INCLUDE=%MSVC%\include;%SDK%\Include\10.0.26100.0\ucrt;%SDK%\Include\10.0.26100.0\shared;%SDK%\Include\10.0.26100.0\um;%EASYX%\include"

