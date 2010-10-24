<% self.seen_css = set() %>

<!DOCTYPE html PUBLIC "XHTML 1.0 Transitional" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html>
        <head>
        	<title>syndicat MeMaTool</title>
            	${self.css()}
        </head>
        <body>
			${self.body()}
        </body>
</html>


<%def name="css_link(path, media='')">
    % if path not in self.seen_css:
        <link rel="stylesheet" type="text/css" href="${path|h}" media="${media}"></link>
    % endif
    <% self.seen_css.add(path) %>
</%def>

<%def name="css()">
	${css_link('/css/main.css', 'screen')}
</%def>
