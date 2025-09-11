param(
  [string]$InputCast = "docs/demo.cast",
  [string]$OutputGif = "docs/demo.gif",
  [int]$Cols = 80,
  [int]$Rows = 24,
  [double]$Speed = 1.1,
  [string]$Theme = "dracula"
)

if (-not (Get-Command agg -ErrorAction SilentlyContinue)) {
  Write-Error "O agregador 'agg' (asciinema-agg) não foi encontrado no PATH. Instale-o e tente novamente."
  exit 1
}

agg -i $InputCast -o $OutputGif --theme $Theme --speed $Speed --cols $Cols --rows $Rows
if ($LASTEXITCODE -eq 0) {
  Write-Host "GIF gerado em $OutputGif" -ForegroundColor Green
}
