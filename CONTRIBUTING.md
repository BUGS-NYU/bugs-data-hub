# Contributing

#### Table of Contents
- [Setup](#user-content-setup)
- [Development](#user-content-development)
- [Comment Annotations](#user-content-comment-annotations)
- [Issue](#user-content-issue)
- [Pull Request](#user-content-pull-request)

## Setup
You'll need to install a few applications to contribute to this project:

- Git
- Python 3
- Reddit API Key

Some of this can be handled for you using the Visual Studio Code.

## Development
To run reddit downloader script, create a `key.json` file with the API key. The file should be formatted like:
```    
"client_id": "YOUR CLIENT ID", 
"client_secret":"YOUR CLIENT SECRET"
```

The script will automatically read the key and download the data.

## Issue
Remember to include enough information if you're reporting a bug.
Asking question through an issue is totally fine as well.

## Pull Request
It would be best to develop your feature with a new branch other than master.
Every PR will be considered.

### Before Creating a PR
- Making sure that the code compiles and test your code.

## Comment Annotations
The codebase uses the following annotations in the comments:

- `@HelpWanted` - We need contributors for this code
- `@TODO` - We need to finish this code
- `@Performance` - This area can be tweaked/rewritten to improve performance
- `@CodeOrg` - We should reorganize this code
