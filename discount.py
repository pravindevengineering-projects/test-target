  def get_discount(price, is_member):
      """Members get 20% off, non-members get 5% off."""
      if not is_member:        # BUG: condition is inverted
          discount = price * 0.20
      else:
          discount = price * 0.05
      return price - discount
      """Members get 20% off, non-members get 5% off."""
      if not is_member:        # BUG: condition is inverted
          discount = price * 0.20
      else:
          discount = price * 0.05
      return price - discount

  def apply_tax(price, rate):
      """Apply tax rate (e.g. 0.08 for 8%)."""
      return price * rate      # BUG: should be price * (1 + rate)
  EOF
