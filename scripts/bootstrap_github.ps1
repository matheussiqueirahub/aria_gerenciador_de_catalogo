param(
  [Parameter(Mandatory=$true)][string]$Owner,
  [Parameter(Mandatory=$true)][string]$Repo,
  [string]$Token = $env:GITHUB_TOKEN,
  [string]$ProjectName = "Roadmap"
)

$ErrorActionPreference = 'Stop'
if (-not $Token) { Write-Error "Informe -Token ou defina GITHUB_TOKEN."; exit 1 }
$base = "https://api.github.com"
$headers = @{ Authorization = "token $Token"; 'User-Agent' = $Owner; 'Accept' = 'application/vnd.github+json'; 'X-GitHub-Api-Version' = '2022-11-28' }

# Labels
$labels = @(
  @{ name='enhancement'; color='a2eeef'; description='New feature or request' },
  @{ name='bug';         color='d73a4a'; description='Something is not working' },
  @{ name='documentation'; color='0075ca'; description='Improvements or additions to documentation' },
  @{ name='tests';       color='0e8a16'; description='Test coverage and scenarios' },
  @{ name='ci';          color='5319e7'; description='Continuous integration' },
  @{ name='help wanted'; color='008672'; description='Extra attention is needed' },
  @{ name='good first issue'; color='7057ff'; description='Good for newcomers' }
)
foreach ($l in $labels) {
  try { Invoke-RestMethod -Method Post -Headers $headers -Uri "$base/repos/$Owner/$Repo/labels" -Body ($l | ConvertTo-Json) | Out-Null } catch { }
}

# Issues
$issues = @(
  @{ title = 'API REST: produtos com FastAPI'; labels=@('enhancement','documentation'); body = "Implementar API REST para produtos:`n- [ ] GET /produtos`n- [ ] POST /produtos`n- [ ] GET /produtos/{id}`n- [ ] PATCH /produtos/{id}`n- [ ] DELETE /produtos/{id}`n`nCritérios:`n- Validações e erros padronizados`n- Retorno JSON`n- Testes básicos (pytest)`n" },
  @{ title = 'Categorias: modelagem e listagem'; labels=@('enhancement'); body = "Adicionar classe Categoria e vincular Produto->Categoria.`n- [ ] CRUD de categorias`n- [ ] Listar produtos por categoria`n- [ ] Ajustar persistência (CSV ou outro)`n" },
  @{ title = 'CLI: validação e UX'; labels=@('enhancement'); body = "Melhorar mensagens de erro e validação de entradas na CLI.`n- [ ] Mensagens claras`n- [ ] Repetição de prompts somente quando necessário`n" },
  @{ title = 'Tests: casos de erro e limites'; labels=@('tests'); body = "Cobrir cenários de borda e erros:`n- [ ] Estoque insuficiente`n- [ ] Preços inválidos`n- [ ] CSV com linhas inválidas`n" },
  @{ title = 'CI: badges e matrix'; labels=@('ci','tests'); body = "Ajustar CI para múltiplas versões do Python e manter badge no README." }
)
foreach ($it in $issues) {
  Invoke-RestMethod -Method Post -Headers $headers -Uri "$base/repos/$Owner/$Repo/issues" -Body ($it | ConvertTo-Json) | Out-Null
}

# Project (classic)
try {
  $projHeaders = $headers.Clone();
  $projHeaders['Accept'] = 'application/vnd.github.inertia-preview+json'
  Invoke-RestMethod -Method Post -Headers $projHeaders -Uri "$base/repos/$Owner/$Repo/projects" -Body (@{ name=$ProjectName; body='Kanban do projeto' } | ConvertTo-Json) | Out-Null
} catch {
  Write-Warning 'Não foi possível criar Project clássico (pode estar desativado).'
}

Write-Host "Bootstrap concluído." -ForegroundColor Green
