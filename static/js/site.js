document.addEventListener("DOMContentLoaded", () => {
  // Confirm potentially destructive actions.
  document.querySelectorAll("[data-confirm]").forEach((element) => {
    element.addEventListener("click", (event) => {
      const message = element.dataset.confirm || "Are you sure?";
      if (!window.confirm(message)) event.preventDefault();
    });
  });
 
  // Keep quantity controls within a sensible range.
  document.querySelectorAll("[data-quantity-control]").forEach((control) => {
    const input = control.querySelector("input");
    const minus = control.querySelector("[data-minus]");
    const plus = control.querySelector("[data-plus]");
    if (!input) return;
 
    minus?.addEventListener("click", () => {
      input.value = Math.max(1, Number(input.value || 1) - 1);
      input.dispatchEvent(new Event("change", { bubbles: true }));
    });
    plus?.addEventListener("click", () => {
      input.value = Math.max(1, Number(input.value || 1) + 1);
      input.dispatchEvent(new Event("change", { bubbles: true }));
    });
  });
});
