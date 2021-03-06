[CmdletBinding()]
param(
	[Parameter(Mandatory=$false)]
	[string]
	$pipFile
)

Write-Host "Starting attempt at upgrading package versions in pip requirements file."
Write-Host "Note that the script performs a pip upgrade in the folder where the requirements file is to try to determin whether there are newer versions."
Write-Host "Therefore, if you use python environments it might be a very good idea to enable them before use."

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
		$pipFileAbsolutePath = Resolve-Path $pipFile
		Push-Location $PSScriptRoot
	}
	else {
		$pipFile = Join-Path -Path $PWD -ChildPath 'requirements.txt'
		# No need to change working directory to the location of the pip file because we're already there
		if(!(Test-Path $pipFile -PathType Leaf)) {
			throw "Did not recieve pip requirements file as parameter. Could not find pip requirements file in script folder nor folder script was called from."
		}
		$pipFileAbsolutePath = Resolve-Path $pipFile
	}
}
else{
	# Get folder from pip file param
	# push location
	$pipFileAbsolutePath = Resolve-Path $pipFile
	$pipFileDirectory = Split-Path -Path $pipFileAbsolutePath -Parent
	Push-Location $pipFileDirectory
}

Write-Debug "Using python version:"
Write-Debug (python --version)
Write-Debug "Using pip version:"
Write-Debug ((pip --version) -join " ")

Write-Debug "Using [$pipFileAbsolutePath] as path to pip file"

$pipFileOriginalContent = (Get-Content $pipFileAbsolutePath)
# `(?m)` is for "multi-line mode". It ensures that the match removing from the first `#` character to the end of line (`n) is applied for every line, rather than for only the first hit in the (possibly multi line) string.
$pipFileWithoutComments = $pipFileOriginalContent -replace "(?m)#.*`n?", ''
Write-Debug "Pip file with all comments removed:"
Write-Debug ($pipFileWithoutComments -join "`n")

# Remove all empty lines and lines only containing whitespace after removing the comments.
# Do it in this order, because removing comments the way it's done above leaves an empty line
$pipFileWithoutEmptyLines = $pipFileWithoutComments -match '\S'
Write-Debug "Pip file with all empty lines removed (should now only be versioned packages):"
Write-Debug ($pipFileWithoutEmptyLines -join "`n")

# Remove all version information, so that we only pass the package names to pip,
# and leave it to pip to pick what's the newest version.
# `[>=]` matches "exactly one of > or ="
$pipPackageNames = $pipFileWithoutEmptyLines -replace "[>=]=.*`n?", ""
Write-Debug "Pip file with all other information than package names removed:"
Write-Debug ($pipPackageNames -join "`n")

Write-Verbose "Installing packages using pip to determin what pip thinks are the newest packages."
if($PSCmdlet.MyInvocation.BoundParameters["Debug"].IsPresent) {
	pip install --upgrade $pipPackageNames
}
else {
	pip install --upgrade $pipPackageNames --quiet
}

$updatedPackages = pip freeze
$pipFileUpdatedContent = $pipFileOriginalContent
Write-Verbose "Replacing all current package versions with package versions pip found to be current and add new dependencies found by PIP."
$newNotPreviouslyInstalledPackages = ""
Foreach($versionedPackage in $updatedPackages) {
	$packageName = $versionedPackage -replace "[>=]=.*", ""
	$packageVersion = $versionedPackage -replace ".*[>=]=", ""
	Write-Debug "Processing package ${packageName} (version ${packageVersion}) found by pip."

	$packagePreviouslyInstalled = $pipFileUpdatedContent -match "(?<=$packageName[>=]=).*"
	if($packagePreviouslyInstalled) {
		Write-Debug "Setting ${packageName} to version ${packageVersion}"
		# Use `-join "`n"` to ensure that the newlines are preserved in the string instead of powershell starting to consider each line a separate string that gets joined togehter weirdly when using the `-NoNewline` option on `Set-Content`.
		$pipFileUpdatedContent = $pipFileUpdatedContent -replace "(?<=$packageName[>=]=).*", $packageVersion -join "`n"
	}
	else{
		Write-Debug "Found new package not previously in requirements file: ${packageName} (version ${packageVersion})"
		$newNotPreviouslyInstalledPackages += $versionedPackage + "`n"
	}
}

if(!($newNotPreviouslyInstalledPackages -eq "")) {
	Write-Verbose "Adding new not previously installed packages to file."
	Write-Debug "List of new dependencies not previously listed in requirements file:"
	Write-Debug ($newNotPreviouslyInstalledPackages -join "`n")

	$dateTimeString = Get-Date -Format "u"
	$pipFileUpdatedContent += "`n`n# New dependencies found by pip ${dateTimeString}:`n"
	$pipFileUpdatedContent += $newNotPreviouslyInstalledPackages
}

if(!($pipFileUpdatedContent.EndsWith("`n"))){
	$pipFileUpdatedContent += "`n"
}

Write-Verbose "Writing packages and versions to requirements file."
# Use `-NoNewline` to ensure that powershell does not add extra newlines between what it interprets to be different objects in the string we are trying to stuff into the file.
# Although the encoding should go out as it out of the box, use `-Encoding UTF8NoBOM` to be very sure of that is being output.
Set-Content -Path $pipFileAbsolutePath -Value $pipFileUpdatedContent -Encoding UTF8NoBOM -NoNewline

Write-Host "Remember to test that upgraded dependencies work before checking in."

Pop-Location
