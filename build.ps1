$ErrorActionPreference = 'Stop'
Push-Location $PSScriptRoot
try {
    function Invoke-CheckedTool {
        param(
            [Parameter(Mandatory = $true)][string]$Name,
            [Parameter(Mandatory = $true)][string[]]$Arguments
        )

        $tool = Get-Command $Name -ErrorAction Stop
        Write-Host "Running $Name $($Arguments -join ' ')"
        $previousErrorAction = $ErrorActionPreference
        $ErrorActionPreference = 'Continue'
        try {
            & $tool.Source @Arguments 2>&1 | ForEach-Object { Write-Host $_ }
            $exitCode = $LASTEXITCODE
        }
        finally {
            $ErrorActionPreference = $previousErrorAction
        }
        if ($exitCode -ne 0) {
            throw "$Name failed with exit code $exitCode"
        }
    }

    # Create the main labels first, then the supplement imports them; the last
    # main passes import the supplement labels through xr.
    $latexArgs = @('-interaction=nonstopmode', '-halt-on-error', '-file-line-error')
    Invoke-CheckedTool 'pdflatex' ($latexArgs + 'paper2.tex')
    Invoke-CheckedTool 'bibtex' @('paper2')
    Invoke-CheckedTool 'pdflatex' ($latexArgs + 'paper2.tex')
    Invoke-CheckedTool 'pdflatex' ($latexArgs + 'paper2_supp.tex')
    Invoke-CheckedTool 'bibtex' @('paper2_supp')
    Invoke-CheckedTool 'pdflatex' ($latexArgs + 'paper2_supp.tex')
    Invoke-CheckedTool 'pdflatex' ($latexArgs + 'paper2_supp.tex')
    Invoke-CheckedTool 'pdflatex' ($latexArgs + 'paper2.tex')
    Invoke-CheckedTool 'pdflatex' ($latexArgs + 'paper2.tex')

    $pdfinfo = Get-Command 'pdfinfo' -ErrorAction SilentlyContinue
    if ($pdfinfo) {
        $previousErrorAction = $ErrorActionPreference
        $ErrorActionPreference = 'Continue'
        try {
            $info = & $pdfinfo.Source 'paper2.pdf' 2>&1
            $infoExitCode = $LASTEXITCODE
        }
        finally {
            $ErrorActionPreference = $previousErrorAction
        }
        if ($infoExitCode -ne 0) {
            throw "pdfinfo failed with exit code $infoExitCode"
        }
        $pageLine = $info | Where-Object { $_.ToString() -match '^Pages:\s+' } | Select-Object -First 1
        if ($pageLine -match '^Pages:\s+(\d+)') {
            $pages = [int]$Matches[1]
            Write-Host "paper2.pdf: $pages pages (20-page maximum)."
            if ($pages -gt 20) {
                throw "paper2.pdf exceeds the 20-page limit ($pages pages)."
            }
        }
    }
    else {
        Write-Host 'pdfinfo is unavailable; check paper2.pdf page count manually.'
    }
}
finally {
    Pop-Location
}
