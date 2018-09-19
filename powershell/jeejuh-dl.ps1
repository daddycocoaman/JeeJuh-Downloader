##################################
###          daddycocoaman     ###
###  https://daddycocoaman.com ###
###  http://twitter.com/mcohmi ###
##################################

#requires -version 3.0

[CmdletBinding()]
Param
(
    [string]$output,
    [Parameter(Mandatory=$true)][string]$url
)

function getLinks ($url) 
{
    $headers = @{}
    $headers.Add('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0')
    $page = Invoke-WebRequest -Uri $url -SessionVariable session -Headers $headers
    return $page.Links | Where-Object {$_.href -like "*downloader.php*"}
}

function downloadFiles($links, $output, $url)
{
    $domain = "https://www.jeejuh.com"
    $headers = @{}
    $headers.Add('Referer', $url)
    $headers.Add('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0')

    foreach ($link in $links)
    {
        $link.outerHTML -match ".*\>(?<name>.*)\</a\>" | Out-Null
        $dlLink = -join ($domain,$link.href)
        $dlLink = $dlLink -replace "amp;", ""
        $name = $Matches['name']
        $trackname = $name.split("-")[1].Trim()

        $path = Join-Path -Path $output -ChildPath $trackname

        if (!(Test-Path $path -PathType Container))
        {
            New-Item -ItemType Directory -Force -Path $path | Out-Null
        }

        $outFile = Join-Path -Path $path -ChildPath $name
        $webClient = New-Object System.Net.WebClient
        $webClient.Headers.add('Referer', $url)
        $webClient.DownloadFile($dlLink, $outFile)
        Write-Host "Saving $name to $outFile..."
    }
}

####################MAIN CODE####################
if ($PsBoundParameters.ContainsKey('output'))
{
    if (!(Test-Path $output -PathType Container))
    {
        New-Item -ItemType Directory -Force -Path $output | Out-Null
    }
}
else {$output = $PWD.Path}

$links = getLinks($url)
downloadFiles $links $output $url
Write-Host ""
Write-Host "Complete!"