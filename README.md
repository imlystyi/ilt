<br/>

<div align="center">
  <a href="https://github.com/imlystyi/ilt">
    <img src="https://github.com/imlystyi/ilt/assets/47981548/fd8bede8-1311-4672-bc6e-27901a7447f4" alt="Coin Manager Logo" width="150" height="150">
  </a>
  
<h3 align="center"><font size="6"> 
ilt
</font></h3>

  <p align="center">
  Insert license text
    <br/>
    <a href="https://github.com/github_username/repo_name"></a>
</div>
 
 ## Why do I need this?
If you license your program, **ilt** will help you insert the text (header) of this license into your source code files, so that you don't have to insert them yourself.
 
 ## Functionality
 - Automatic insertion of license texts into source code files (if the extension of such a file and the format of comments are known by **ilt**)
 - Special insertion if you want to change startline format (or if the extension of such a file and the format of comments aren't known by **ilt**)

## How can I use it?
- If you want to do automatic insertion, use this command:
```
auto <license_name> "<path>" <year> "<copyright_holder>" "<special_line>" "<ignored_folders>" "<ignored_exts>" <keys>
```

- If you want to do special insertion into the specified file, use this command:
```
special <license_name> "<path_to_file>" "<comments_format>" <year> "<copyright_holder>" "<special_line>"
```
- If you want to do special insertion into the files with the specified extension, use this command:
```
special <license_name> "<path_to_root_folder>" "ignored_folders" "<extension>" "<comments_format>" <year> "<copyright_holder>" "<special_line>"
```
- **Use the `help` command to view detailed help for all commands.**

## Avaliable licenses (and their texts)
**THE LICENSES AND THE TEXTS OF THESE LICENSES ARE NOT THE PROPERTY OF THE SOFTWARE AUTHOR!**

 1. Apache License 2.0 (apache)
 2. Boost Software License (bsl)
 3. BSD 2-Clause License (bsd2)
 4. BSD 3-Clause License (bsd3)
 5. GNU Affero Public License v3.0 (agpl)
 6. GNU General Public License v2.0 (gpl2)
 7. GNU General Public License v3.0 (gpl3)
 8. GNU Lesser General Public License v2.1 (lgpl)
 9. MIT License (mit)
 10. The Unlicense (unlicense) 

Want to see a new license? Offer it in [Issues](https://github.com/imlystyi/ilt/issues/new)!

## Avaliable codefile extensions in the automatical mode
1. C: `.c`
2. C++: `cpp`,`.cc`,`.cpp`,`.cxx`
3. C#: `.cs`
4. Delphi: `.dpr`,`.drc`
5. Fortran: `.f`,`.for`,`.f95`
6. Go: `.go`
7. Java: `.java`
8. JavaScript: `.js`
9. PHP: `.php`
10. Python: `.py`,`.pyc`,`.pyi`
11. Ruby: `.rb` 
12. Swift: `.swift` 
13. TypeScript: `.ts`
14. Visual Basic: `.vb`

Want to see a new extension? Offer it in [Issues](https://github.com/imlystyi/ilt/issues/new)!
