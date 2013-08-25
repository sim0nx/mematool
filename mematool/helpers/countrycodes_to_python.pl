#!/usr/bin/perl -w

open(FH, "countrycodes.txt");

print "cc = {";

while (<FH>)
{
  if (/(\w{2})\s+(.*)/)
  {
    print "\"$1\": \"$2\",\n";
  }
}

print "}";
