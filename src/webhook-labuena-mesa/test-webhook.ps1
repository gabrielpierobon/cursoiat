# Script de prueba para el webhook de La Buena Mesa
# Ejecutar desde PowerShell con: .\test-webhook.ps1
# 
# IMPORTANTE: Para que los acentos se muestren correctamente:
# 1. Ejecute PowerShell como administrador
# 2. Ejecute el siguiente comando antes de usar este script: 
#    [Console]::OutputEncoding = [System.Text.Encoding]::UTF8
# 3. Cambie el tipo de letra de la consola a una que soporte Unicode (como Consolas)

# Intentar configurar la codificación UTF-8 (puede requerir permisos de administrador)
try {
    [Console]::OutputEncoding = [System.Text.Encoding]::UTF8
    $PSDefaultParameterValues['Out-File:Encoding'] = 'utf8'
    $PSDefaultParameterValues['*:Encoding'] = 'utf8'
    [System.Console]::OutputEncoding = [System.Text.Encoding]::UTF8
    chcp 65001 | Out-Null # Cambiar a UTF-8 en la consola CMD subyacente
    Write-Host "Codificacion UTF-8 configurada correctamente" -ForegroundColor Green
}
catch {
    Write-Host "AVISO: No se pudo configurar la codificacion UTF-8 automaticamente" -ForegroundColor Yellow
    Write-Host "Para ver acentos correctamente, ejecute PowerShell como administrador" -ForegroundColor Yellow
    Write-Host "y ejecute: [Console]::OutputEncoding = [System.Text.Encoding]::UTF8" -ForegroundColor Yellow
    Start-Sleep -Seconds 3
}

# Función para decodificar correctamente las respuestas del servidor
function Format-Response {
    param (
        [Parameter(Mandatory=$true)]
        [PSCustomObject]$Response
    )
    
    # Si la respuesta contiene "fulfillmentText", decodificar su valor
    if ($Response.PSObject.Properties.Name -contains "fulfillmentText") {
        $text = $Response.fulfillmentText
        
        # Diccionario simple de reemplazos para caracteres acentuados
        $reemplazos = @{
            "Ã¡" = "á"
            "Ã©" = "é"
            "Ã­" = "í"
            "Ã³" = "ó"
            "Ãº" = "ú"
            "Ã±" = "ñ"
            "Â¡" = "¡"
            "Â¿" = "¿"
            "Ã" = "Á"
        }
        
        # Aplicar reemplazos
        foreach ($key in $reemplazos.Keys) {
            $text = $text.Replace($key, $reemplazos[$key])
        }
        
        # Crear un objeto nuevo con el texto corregido
        $newResponse = [PSCustomObject]@{
            fulfillmentText = $text
        }
        return $newResponse
    }
    
    return $Response
}

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
        
        # Usar un email y teléfono aleatorios para evitar duplicados
        $random = Get-Random -Minimum 1000 -Maximum 9999
        $email = "usuario$random@ejemplo.com"
        $telefono = "+346789$random"
        
        $body = @{
            queryResult = @{
                intent = @{
                    displayName = "register_club_member"
                }
                parameters = @{
                    nombre = "Carlos Mendez Gomez"  # Nombre sin acentos para evitar problemas
                    email = $email
                    telefono = $telefono
                }
            }
        } | ConvertTo-Json -Depth 5

        # Convertir explícitamente a UTF-8 para asegurar compatibilidad con caracteres acentuados
        $bodyBytes = [System.Text.Encoding]::UTF8.GetBytes($body)
        
        try {
            $response = Invoke-RestMethod -Uri "$baseUrl/webhook" -Method Post -Body $bodyBytes -ContentType "application/json; charset=utf-8"
            
            # Formatear y mostrar la respuesta
            Write-Host "Respuesta del servidor (original):" -ForegroundColor Yellow
            $response | ConvertTo-Json
            
            Write-Host "Respuesta del servidor (corregida):" -ForegroundColor Green
            $formattedResponse = Format-Response -Response $response
            $formattedResponse | ConvertTo-Json
            
            # Guardar información para verificación
            Write-Host "`nInformación del registro:" -ForegroundColor Cyan
            Write-Host "Nombre: Carlos Mendez Gomez" -ForegroundColor White
            Write-Host "Email: $email" -ForegroundColor White
            Write-Host "Teléfono: $telefono" -ForegroundColor White
        }
        catch {
            Write-Host "Error al registrar miembro: $_" -ForegroundColor Red
        }
    }
    "3" {
        Write-Host "Registrando nuevo miembro (formato complejo)..." -ForegroundColor Cyan
        
        # Usar un email y teléfono aleatorios para evitar duplicados
        $random = Get-Random -Minimum 1000 -Maximum 9999
        $email = "ana$random@ejemplo.com"
        $telefono = "+346543$random"
        
        $body = @{
            queryResult = @{
                intent = @{
                    displayName = "register_club_member"
                }
                parameters = @{
                    nombre = @{ name = "Ana Garcia Lopez" }  # Nombre sin acentos
                    email = @{ email = $email }
                    telefono = @{ number = $telefono }
                }
            }
        } | ConvertTo-Json -Depth 5

        # Convertir explícitamente a UTF-8
        $bodyBytes = [System.Text.Encoding]::UTF8.GetBytes($body)
        
        try {
            $response = Invoke-RestMethod -Uri "$baseUrl/webhook" -Method Post -Body $bodyBytes -ContentType "application/json; charset=utf-8"
            
            # Formatear y mostrar la respuesta
            Write-Host "Respuesta del servidor (original):" -ForegroundColor Yellow
            $response | ConvertTo-Json
            
            Write-Host "Respuesta del servidor (corregida):" -ForegroundColor Green
            $formattedResponse = Format-Response -Response $response
            $formattedResponse | ConvertTo-Json
            
            # Guardar información para verificación
            Write-Host "`nInformación del registro:" -ForegroundColor Cyan
            Write-Host "Nombre: Ana Garcia Lopez" -ForegroundColor White
            Write-Host "Email: $email" -ForegroundColor White
            Write-Host "Teléfono: $telefono" -ForegroundColor White
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

        # Convertir explícitamente a UTF-8
        $bodyBytes = [System.Text.Encoding]::UTF8.GetBytes($body)
        
        try {
            Write-Host "Enviando solicitud..." -ForegroundColor Cyan
            Write-Host "Payload:" -ForegroundColor Gray
            $body
            
            $response = Invoke-RestMethod -Uri "$baseUrl/webhook" -Method Post -Body $bodyBytes -ContentType "application/json; charset=utf-8"
            
            # Formatear y mostrar la respuesta
            Write-Host "Respuesta del servidor (original):" -ForegroundColor Yellow
            $response | ConvertTo-Json
            
            Write-Host "Respuesta del servidor (corregida):" -ForegroundColor Green
            $formattedResponse = Format-Response -Response $response
            $formattedResponse | ConvertTo-Json
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
Write-Host "NOTA: Si viste problemas con los acentos, ejecuta PowerShell como administrador" -ForegroundColor Yellow
Write-Host "y ejecuta este comando: [Console]::OutputEncoding = [System.Text.Encoding]::UTF8" -ForegroundColor Yellow
Write-Host ""
Write-Host "Presiona cualquier tecla para salir..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown") 