[CmdletBinding()]
param(
	[Parameter(Mandatory=$false)]
	[string]
	$pipFile
)

if($pipFile -eq "") {
	# Pip file was not present.
	# Start with assuming the pip file is in the same folder as this script (and is called requirements.txt).
	# If that fails, check the location the script was called from.
	# If that fails, throw, because wtf is the user actually trying to do?

	# $PSScriptRoot
	# Test-Path $path -PathType Leaf
	# Join-Path -Path 'c:\windows' -ChildPath $folder
	$pipFile = Join-Path -Path $PSScriptRoot -ChildPath 'requirements.txt'
	if(Test-Path $pipFile -PathType Leaf) {
		Push-Location $PSScriptRoot
	}
	else {
		$pipFile = Join-Path -Path $PWD -ChildPath 'requirements.txt'
		# No need to change working directory to the location of the pip file because we're already there
		if(!(Test-Path $pipFile -PathType Leaf)) {
			throw "Did not recieve pip requirements file as parameter. Could not find pip requirements file in script folder nor folder script was called from."
		}
	}
}
else{
	# Get folder from pip file param
	# push location
	$pipFileDirectory = Split-Path -Path $pipFile -Parent
	Push-Location $pipFileDirectory
}

$pipFileAbsolutePath = Resolve-Path $pipFile

$pipFileOriginalContent = (Get-Content $pipFileAbsolutePath)
$pipFileWithoutComments = $pipFileOriginalContent -replace "(?m)#.*`n?", ''
$pipFileWithoutEmptyLines = $pipFileWithoutComments -match '\S'
$pipPackageNames = $pipFileWithoutEmptyLines -replace "==.*`n?", ""

Write-Verbose "Installing packages using pip to determin what pip thinks are the newest packages"
pip install -U $pipPackageNames
$updatedPackages = pip freeze
$pipFileUpdatedContent = $pipFileOriginalContent
Write-Verbose "Replacing all current package versions with package versions pip found to be current."
Foreach($versionedPackage in $updatedPackages) {
	$packageName = $versionedPackage -replace "==.*", ""
	$packageVersion = $versionedPackage -replace ".*==", ""
	Write-Host "Setting $packageName to version $packageVersion"

	$pipFileUpdatedContent = $pipFileUpdatedContent -replace "(?<=$packageName==).*", $packageVersion
}

Write-Verbose "Writing new packages to requirements file."
Set-Content $pipFileAbsolutePath $pipFileUpdatedContent

Write-Host "Remember to test that upgraded dependencies work before checking in."

Pop-Location
