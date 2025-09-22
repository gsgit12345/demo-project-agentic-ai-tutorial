from mcp.server.fastmcp import FastMCP

mcp=FastMCP("Math")

@mcp.tool()
def  add(a:int,b:int)->int:

    if a==0 or b==0:
        raise ValueError("a and b are zero.can not add")
    return a+b

@mcp.tool()
def  divide(a:int,b:int)->int:

    if a==0 or b==0:
        raise ValueError("a and b are zero.can not add")
    return a/b
@mcp.tool()
def  multiply(a:int,b:int)->int:

    if a==0 or b==0:
        raise ValueError("a and b are zero.can not add")
    return a*b

@mcp.tool()
def  mod(a:int,b:int)->int:

    if a==0 or b==0:
        raise ValueError("a and b are zero.can not add")
    return a%b

if __name__=="__main__":
   #mcp.run(transport="stdio")
   mcp.run(transport="streamable-http")   # if your mcp server code is not available on the local machine