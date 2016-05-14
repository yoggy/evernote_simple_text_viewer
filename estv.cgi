#!/usr/bin/ruby
# -*- coding: utf-8 -*-
#
# estv.cgi - Evernote Simple Text Viewer (for Publich Shared Note)
#
# parameters:
#     path : the path included shared note url 
#
# examples:
#     shared note url : https://www.evernote.com/shard/s2/sh/96854163-699b-41b8-9ade-a39a0026de16/d48bed79a31a0f13
#       ↓
#     http://example.com/path/to/cgi/estv.cgi?path=/shard/s2/sh/96854163-699b-41b8-9ade-a39a0026de16/d48bed79a31a0f13
#
# github:
#     https://github.com/yoggy/evernote_simple_text_viewer
#
# license:
#     Copyright (c) 2016 yoggy <yoggy0@gmail.com>
#     Released under the MIT license
#     http://opensource.org/licenses/mit-license.php;
#

require 'cgi'
require 'open-uri'
require 'nokogiri'
require 'pp'

cgi = CGI.new

base_url = 'https://www.evernote.com'
path = cgi['path']
param = '?content='

referer_url = base_url + path
content_url = base_url + path + param

# get note title
note_title = ''
begin
  doc = Nokogiri::HTML(open(referer_url), nil, 'UTF-8')
  note_title = doc.css('.note-title').inner_text
rescue Exception => e
  note_title = '<div>' + CGI.escapeHTML(e.to_s) + '</div>'
end

# get note content
ennote_html = ''
begin
  doc = Nokogiri::HTML(open(content_url, 'Referer' => referer_url), nil, 'UTF-8')
  ennote_html = doc.css('.ennote').inner_html
rescue Exception => e
  ennote_html = '<div>' + CGI.escapeHTML(e.to_s) + '</div>'
end

# remove <div> tag
ennote_html.gsub!(/<div>/, '')
ennote_html.gsub!(/<div (.+?)>/, '')
ennote_html.gsub!(/<br>/, '')
ennote_html.gsub!(/<\/div>/, '')

# special format rule
# (extract the part surrounded by ====)
slice = ennote_html.scan(/====\n(.*)====/m)
if slice != nil && slice.size > 0
  ennote_html = slice[0][0]
end

# send response
puts cgi.header("charset" => "utf-8")
puts <<-EOS_HEAD
<html>
  <head>
    <meta charset="UTF-8">
    <meta http-equiv="refresh" content="180">
    <title>#{CGI.escapeHTML(note_title)}</title>
    <style type="text/css">
      <!--
      body {
        font-size: 2em
        font-family: sans-serif
      }
      -->
    </style>
  </head>
  </head>
  <body>
EOS_HEAD

print '<pre>'
puts ennote_html
puts '</pre></body></html>'

