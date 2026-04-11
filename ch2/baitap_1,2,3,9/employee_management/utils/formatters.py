class Formatters:
    """
    Tiện ích định dạng dữ liệu để hiển thị cho người dùng.
    """
    @staticmethod
    def format_currency(amount: float) -> str:
        """Định dạng số tiền sang chuẩn VNĐ."""
        return f"{amount:,.0f} VNĐ"

    @staticmethod
    def format_header(title: str) -> str:
        """Tạo tiêu đề được bao quanh bởi các đường gạch ngang."""
        line = "=" * 60
        return f"\n{line}\n{title.center(60)}\n{line}"
