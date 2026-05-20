@echo off
setlocal EnableExtensions EnableDelayedExpansion

:: ===== Configuração/ajuda =====
if /I "%~1"=="-h"  goto :help
if /I "%~1"=="/h"  goto :help
if /I "%~1"=="--help" goto :help

:: Pasta raiz = 1º argumento ou pasta atual
set "ROOT=%~1"
if not defined ROOT set "ROOT=%cd%"

:: Checa flag /dry-run em qualquer argumento
set "DRYRUN="
for %%A in (%*) do (
  if /I "%%~A"=="/dry-run" set "DRYRUN=1"
)

:: Normaliza ROOT removendo aspas extras
for %%# in ("%ROOT%") do set "ROOT=%%~f#"

if not exist "%ROOT%" (
  echo [ERRO] Pasta nao encontrada: "%ROOT%"
  exit /b 1
)

:: ===== Timestamp e log =====
set "TS=%date%_%time%"
set "TS=%TS:/=%"
set "TS=%TS::=%"
set "TS=%TS:.=%"
set "TS=%TS:,=%"
set "TS=%TS: =0%"
set "LOG=%ROOT%\cleanup_pycache_%TS%.log"

echo ================================================== > "%LOG%"
echo Limpeza de __pycache__                              >> "%LOG%"
echo Pasta raiz: "%ROOT%"                                >> "%LOG%"
if defined DRYRUN (echo Modo: DRY-RUN (apenas listar)    >> "%LOG%") else (echo Modo: EXECUTANDO REMOCOES >> "%LOG%")
echo Iniciado: %date% %time%                             >> "%LOG%"
echo ================================================== >> "%LOG%"

set /a FOUND=0, OK=0, ERR=0

:: ===== Procura e (opcionalmente) remove =====
for /d /r "%ROOT%" %%D in (__pycache__) do (
  set /a FOUND+=1
  if defined DRYRUN (
    echo [LISTAR] "%%~fD"
    >>"%LOG%" echo [LISTAR] "%%~fD"
  ) else (
    echo [APAGAR] "%%~fD"
    rd /s /q "%%~fD" 1>nul 2>nul
    if exist "%%~fD" (
      set /a ERR+=1
      >>"%LOG%" echo [FALHA] "%%~fD"
    ) else (
      set /a OK+=1
      >>"%LOG%" echo [OK] "%%~fD"
    )
  )
)

echo.>>"%LOG%"
echo Pastas encontradas: %FOUND%   >> "%LOG%"
echo Removidas com sucesso: %OK%   >> "%LOG%"
echo Falhas: %ERR%                 >> "%LOG%"
echo Finalizado: %date% %time%     >> "%LOG%"

:: ===== Resumo no console =====
echo.
echo ===== RESUMO =====
echo Pasta raiz: "%ROOT%"
if defined DRYRUN (echo Modo: DRY-RUN ^(nao removeu nada^))
echo Pastas encontradas: %FOUND%
if not defined DRYRUN (
  echo Removidas com sucesso: %OK%
  echo Falhas: %ERR%
)
echo Log salvo em: "%LOG%"
exit /b 0

:help
echo Uso:
echo   cleanup_pycache.bat  [PASTA_RAIZ]  [/dry-run]
echo.
echo Ex.:  cleanup_pycache.bat "D:\Projetos\MeuApp"
echo Ex.:  cleanup_pycache.bat /dry-run
echo Ex.:  cleanup_pycache.bat "D:\Repos" /dry-run
exit /b 0
