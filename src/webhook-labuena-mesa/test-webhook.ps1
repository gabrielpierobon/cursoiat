# Script de prueba para el webhook de La Buena Mesa
# Ejecutar desde PowerShell con: .\test-webhook.ps1

Write-Host "=== PRUEBA DE WEBHOOK LA BUENA MESA ===" -ForegroundColor Cyan
Write-Host "Selecciona la prueba que deseas realizar:" -ForegroundColor Yellow
Write-Host "1. Verificar estado del servidor (GET /)"
Write-Host "2. Registrar nuevo miembro (básico)"
Write-Host "3. Registrar nuevo miembro (formato complejo)"
Write-Host "4. Iniciar prueba interactiva (ingresa tus propios datos)"
Write-Host ""

$option = Read-Host "Selecciona una opción (1-4)"

# URL base del servidor
$baseUrl = "http://localhost:8000"

switch ($option) {
    "1" {
        Write-Host "Verificando estado del servidor..." -ForegroundColor Cyan
        try {
            $response = Invoke-RestMethod -Uri $baseUrl -Method Get
            Write-Host "Respuesta del servidor:" -ForegroundColor Green
            $response | ConvertTo-Json
        }
        catch {
            Write-Host "Error al conectar con el servidor: $_" -ForegroundColor Red
        }
    }
    "2" {
        Write-Host "Registrando nuevo miembro (formato básico)..." -ForegroundColor Cyan
        
        $body = @{
            queryResult = @{
                intent = @{
                    displayName = "register_club_member"
                }
                parameters = @{
                    nombre = "Carlos Mendoza"
                    email = "carlos@ejemplo.com"
                    telefono = "+34123456789"
                }
            }
        } | ConvertTo-Json -Depth 5
        
        try {
            $response = Invoke-RestMethod -Uri "$baseUrl/webhook" -Method Post -Body $body -ContentType "application/json"
            Write-Host "Respuesta del servidor:" -ForegroundColor Green
            $response | ConvertTo-Json
        }
        catch {
            Write-Host "Error al registrar miembro: $_" -ForegroundColor Red
        }
    }
    "3" {
        Write-Host "Registrando nuevo miembro (formato complejo)..." -ForegroundColor Cyan
        
        $body = @{
            queryResult = @{
                intent = @{
                    displayName = "register_club_member"
                }
                parameters = @{
                    nombre = @{ name = "Ana García" }
                    email = @{ email = "ana@ejemplo.com" }
                    telefono = @{ number = "+34987654321" }
                }
            }
        } | ConvertTo-Json -Depth 5
        
        try {
            $response = Invoke-RestMethod -Uri "$baseUrl/webhook" -Method Post -Body $body -ContentType "application/json"
            Write-Host "Respuesta del servidor:" -ForegroundColor Green
            $response | ConvertTo-Json
        }
        catch {
            Write-Host "Error al registrar miembro: $_" -ForegroundColor Red
        }
    }
    "4" {
        Write-Host "Prueba interactiva - Ingresa los datos del nuevo miembro:" -ForegroundColor Cyan
        $nombre = Read-Host "Nombre"
        $email = Read-Host "Email"
        $telefono = Read-Host "Teléfono (con código de país, ej: +34612345678)"

        Write-Host "Selecciona el formato:" -ForegroundColor Yellow
        Write-Host "1. Básico (string simple)"
        Write-Host "2. Complejo (objeto)"
        $formatOption = Read-Host "Opción"

        if ($formatOption -eq "1") {
            $bodyParams = @{
                nombre = $nombre
                email = $email
                telefono = $telefono
            }
        }
        else {
            $bodyParams = @{
                nombre = @{ name = $nombre }
                email = @{ email = $email }
                telefono = @{ number = $telefono }
            }
        }

        $body = @{
            queryResult = @{
                intent = @{
                    displayName = "register_club_member"
                }
                parameters = $bodyParams
            }
        } | ConvertTo-Json -Depth 5

        try {
            Write-Host "Enviando solicitud..." -ForegroundColor Cyan
            Write-Host "Payload:" -ForegroundColor Gray
            $body
            
            $response = Invoke-RestMethod -Uri "$baseUrl/webhook" -Method Post -Body $body -ContentType "application/json"
            Write-Host "Respuesta del servidor:" -ForegroundColor Green
            $response | ConvertTo-Json
        }
        catch {
            Write-Host "Error al registrar miembro: $_" -ForegroundColor Red
        }
    }
    default {
        Write-Host "Opción no válida" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "Presiona cualquier tecla para salir..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown") 