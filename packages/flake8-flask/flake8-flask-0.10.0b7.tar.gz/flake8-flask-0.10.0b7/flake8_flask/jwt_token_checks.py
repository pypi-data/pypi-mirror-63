import ast
import logging
import sys

from flake8_flask.flask_base_visitor import FlaskBaseVisitor

logger = logging.getLogger(__file__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(stream=sys.stderr)
handler.setFormatter(
    logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
)
logger.addHandler(handler)

SUPPORTED_JWT_MODULES = ["flask_jwt", "flask_jwt_simple", "flask_jwt_extended"]
SUPPORTED_JWT_DECORATORS = [
    "jwt_required",
    "jwt_optional",
    "fresh_jwt_required",
    "jwt_refresh_token_required",
]
SUPPORTED_JWT_CALLS = [
    "JWT",
    "get_jwt_identity",
    "get_current_user",
    "create_refresh_token",
    "create_access_token",
    "set_access_cookies",
    "get_jwt_claims",
    "verify_jwt_in_request",
    "current_identity",
    "decode_token",
    "JWTManager",
]


class JWTTokenChecksVisitor(FlaskBaseVisitor):
    name = "r2c-flask-missing-jwt-token"

    jwt_token_message = f"{name} This file has `flask_jwt`, `flask_jwt_extended`, or `flask_jwt_simple` imported, but no authentication protection with `@jwt_required` or `@jwt_optional`. This means JWT tokens aren't being checked for access to your API routes, which may be a security oversight."

    reported = False

    def __init__(self):
        super(JWTTokenChecksVisitor, self).__init__()

    def _is_jwt_decorator_present(self, node: ast.FunctionDef) -> bool:
        name_list = []

        for decorator in node.decorator_list:
            d = decorator.func if isinstance(decorator, ast.Call) else decorator
            name_list.append(d.attr if isinstance(d, ast.Attribute) else d.id)

        return any(
            [
                name == decorator
                for name in name_list
                for decorator in SUPPORTED_JWT_DECORATORS
            ]
        )

    def _remove_message(self) -> None:
        for node in self.report_nodes:
            if node["message"] == self.jwt_token_message:
                self.report_nodes.remove(node)
                return

    def generic_visit(self, node: ast.AST) -> None:
        ast.NodeVisitor.generic_visit(self, node)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        if not any([self.is_imported(i) for i in SUPPORTED_JWT_MODULES]):
            return

        if not self.reported:
            self.report_nodes.append(
                {"node": node, "message": self.jwt_token_message,}
            )
            self.reported = True

        if self._is_jwt_decorator_present(node):
            self._remove_message()
            return

        self.generic_visit(node)

    def visit_Call(self, node: ast.Call) -> None:
        if not any([self.is_imported(i) for i in SUPPORTED_JWT_MODULES]):
            return

        if isinstance(node.func, ast.Attribute):
            call = node.func.attr
        elif isinstance(node.func, ast.Name):
            call = node.func.id
        else:
            call = ""

        if call in SUPPORTED_JWT_CALLS:
            self.reported = True
            self._remove_message()
            return

        self.generic_visit(node)
