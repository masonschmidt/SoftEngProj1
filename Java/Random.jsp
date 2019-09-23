<%@ page language="java" contentType="text/html"%>
<%@ page import="java.text.*,java.lang.Math" %>
<html>
	<head>
		<title>Date JSP</title>
	</head>
<% int random_num= (int)(Math.random()*1000000+1); %>
<body>
	<h1><%= random_num %></h1>
</body>
</html>
