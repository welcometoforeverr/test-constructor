/* PR6: small functional script connected using Django's static tag. */
document.addEventListener("DOMContentLoaded", () => {
    const toggle = document.getElementById("contrast-toggle");
    if (!toggle) return;
    toggle.addEventListener("click", () => {
        const enabled = document.documentElement.classList.toggle(
            "high-contrast"
        );
        toggle.setAttribute("aria-pressed", String(enabled));
        toggle.textContent = enabled ? "Обычный вид" : "Контраст";
    });
});
