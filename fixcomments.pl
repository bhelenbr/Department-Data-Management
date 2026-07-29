#!/usr/bin/env perl
use strict;
use warnings;

# Usage: perl remove_comments.pl input.bib > output.bib
# Removes @comment{...} blocks, but ONLY when the character
# immediately following the opening brace is '@'.
# Handles nested braces within the block.

die "Usage: $0 file.bib\n" unless @ARGV == 1;

open my $fh, '<', $ARGV[0] or die "Cannot open $ARGV[0]: $!\n";
local $/;                # slurp mode
my $text = <$fh>;
close $fh;

my $out = '';
my $pos = 0;
my $len = length($text);

while ($pos < $len) {
    if ($text =~ /\G(.*?)(\@comment\s*\{)/gcis) {
        my $prefix     = $1;
        my $open_match = $2;
        my $brace_pos  = pos($text) - 1;   # index of the '{' itself

        # Check the character right after the opening brace
        my $next_char = substr($text, $brace_pos + 1, 1);

        if ($next_char eq '@') {
            # This is a block we want to remove.
            $out .= $prefix;

            my $depth = 1;
            my $i = $brace_pos + 1;
            while ($i < $len && $depth > 0) {
                my $c = substr($text, $i, 1);
                if ($c eq '{') {
                    $depth++;
                } elsif ($c eq '}') {
                    $depth--;
                }
                $i++;
            }

            if ($depth != 0) {
                die "Unbalanced braces: no matching '}' for \@comment{ at position $brace_pos\n";
            }

            pos($text) = $i;
            $pos = $i;
        }
        else {
            # Not the pattern we want to remove; keep it as-is
            # and continue scanning right after this opening brace.
            $out .= $prefix . $open_match;
            pos($text) = $brace_pos + 1;
            $pos = $brace_pos + 1;
        }
    }
    else {
        $out .= substr($text, $pos);
        last;
    }
}

print $out;