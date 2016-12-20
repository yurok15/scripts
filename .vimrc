" enable syntax highlighting
syntax enable
colo slate
highlight Comment ctermbg=DarkMagenta
" show line numbers
set number
" set tabs to have 4 spaces
set ts=4
" indent when moving to the next line while writing code
set autoindent
" expand tabs into spaces
set expandtab
" when using the >> or << commands, shift lines by 4 spaces
set shiftwidth=4
" show the matching part of the pair for [] {} and ()
set showmatch
" enable all Python syntax highlighting features
let python_highlight_all = 1
"set ls=2             " status bar
set hlsearch " search highlight
nnoremap <silent> <F5> :!clear;python %<CR>
