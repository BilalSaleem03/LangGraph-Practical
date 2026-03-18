# arithmetic_server_advanced.py
from fastmcp import FastMCP
from pydantic import BaseModel
from typing import Union, Optional
import math

# Define input models
class ArithmeticInput(BaseModel):
    a: float
    b: float

class CalculationResult(BaseModel):
    operation: str
    a: Optional[float] = None
    b: Optional[float] = None
    result: Optional[float] = None
    error: Optional[str] = None
    formatted: Optional[str] = None

# Create MCP server
mcp = FastMCP("Advanced Arithmetic Server")

@mcp.tool()
def power(base: float, exponent: float) -> CalculationResult:
    """
    Calculate base raised to the power of exponent.
    
    Args:
        base: The base number
        exponent: The exponent
    """
    try:
        result = math.pow(base, exponent)
        return CalculationResult(
            operation="power",
            a=base,
            b=exponent,
            result=result,
            formatted=f"{base} ^ {exponent} = {result}"
        )
    except Exception as e:
        return CalculationResult(operation="power", error=str(e))

@mcp.tool()
def sqrt(number: float) -> CalculationResult:
    """
    Calculate the square root of a number.
    
    Args:
        number: The number to find square root of
    """
    try:
        if number < 0:
            return CalculationResult(
                operation="square_root",
                a=number,
                error="Cannot calculate square root of negative number"
            )
        result = math.sqrt(number)
        return CalculationResult(
            operation="square_root",
            a=number,
            result=result,
            formatted=f"√{number} = {result}"
        )
    except Exception as e:
        return CalculationResult(operation="square_root", error=str(e))

@mcp.tool()
def modulus(a: float, b: float) -> CalculationResult:
    """
    Calculate remainder of division (a % b).
    
    Args:
        a: Dividend
        b: Divisor
    """
    try:
        if b == 0:
            return CalculationResult(
                operation="modulus",
                a=a,
                b=b,
                error="Modulus by zero is not allowed"
            )
        result = a % b
        return CalculationResult(
            operation="modulus",
            a=a,
            b=b,
            result=result,
            formatted=f"{a} % {b} = {result}"
        )
    except Exception as e:
        return CalculationResult(operation="modulus", error=str(e))

# Include all basic operations from the simple version
@mcp.tool()
def add(a: float, b: float) -> CalculationResult:
    """Add two numbers."""
    result = a + b
    return CalculationResult(
        operation="addition",
        a=a,
        b=b,
        result=result,
        formatted=f"{a} + {b} = {result}"
    )

@mcp.tool()
def subtract(a: float, b: float) -> CalculationResult:
    """Subtract b from a."""
    result = a - b
    return CalculationResult(
        operation="subtraction",
        a=a,
        b=b,
        result=result,
        formatted=f"{a} - {b} = {result}"
    )

@mcp.tool()
def multiply(a: float, b: float) -> CalculationResult:
    """Multiply two numbers."""
    result = a * b
    return CalculationResult(
        operation="multiplication",
        a=a,
        b=b,
        result=result,
        formatted=f"{a} × {b} = {result}"
    )

@mcp.tool()
def divide(a: float, b: float) -> CalculationResult:
    """Divide a by b."""
    if b == 0:
        return CalculationResult(
            operation="division",
            a=a,
            b=b,
            error="Division by zero is not allowed"
        )
    result = a / b
    return CalculationResult(
        operation="division",
        a=a,
        b=b,
        result=result,
        formatted=f"{a} ÷ {b} = {result}"
    )

# Run the server
if __name__ == "__main__":
    print("🚀 Starting Advanced Arithmetic MCP Server...")
    print("📊 Available tools:")
    print("  ➕ add(a, b) - Addition")
    print("  ➖ subtract(a, b) - Subtraction")
    print("  ✖️ multiply(a, b) - Multiplication")
    print("  ➗ divide(a, b) - Division")
    print("  ^ power(base, exponent) - Power")
    print("  √ sqrt(number) - Square root")
    print("  % modulus(a, b) - Modulus/remainder")
    print("\n" + "="*50)
    mcp.run()