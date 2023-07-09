// px to rem
const calcRem = (px) => `${px / 16}rem`;

const lightColor = {
    red: "#dc3545",
    orange: "#fd7e14",
    yellow: "#ffc107",
    green: "#28a745",
    teal: "#20c997",
    blue: "#007bff",
    indigo: "#6610f2",
    purple: "#6f42c1",
    pink: "#e83e8c",
    cyan: "#17a2b8",
    primary: "#007bff",
    secondary: "#6c757d",
    success: "#28a745",
    info: "#17a2b8",
    warning: "#ffc107",
    danger: "#dc3545",
    vivamagenta: "#be3455",
    graysand: "#e5ccb0",
    graylilac: "#d4cacd",
    agategray: "#b4b1a1",
    palekhaki: "#bfb092",
    paledogwood: "#edcdc2",
    pleinair: "#bfcad6",
    background: "rgba(256, 256, 256, 0.9)",
};

const darkColor = {
    ...lightColor,
    // dark에서만 사용할 color를 자율적으로 추가.
};

const fontSizes = {
    xsmall: calcRem(12),
    small: calcRem(14),
    base: calcRem(16), // 1rem
    lg: calcRem(18),
    xl: calcRem(20),
    xxl: calcRem(22),
    xxxl: calcRem(24),
    xxxxl: calcRem(16 * 2),
    xxxxxl: calcRem(16 * 3),
};

const paddings = {
    xxsmall: calcRem(4),
    xsmall: calcRem(6),
    small: calcRem(8),
    base: calcRem(10),
    lg: calcRem(12),
    xl: calcRem(14),
    xxl: calcRem(16),
    xxxl: calcRem(18),
    xxxxl: calcRem(24),
    xxxxxl: calcRem(36),
    global: calcRem(16 * 6),
};

const margins = {
    small: calcRem(8),
    base: calcRem(10),
    lg: calcRem(12),
    xl: calcRem(14),
    xxl: calcRem(16),
    xxxl: calcRem(18),
    xxxxl: calcRem(24),
    xxxxxl: calcRem(28),
    global: calcRem(16 * 6),
};

const deviceSizes = {
    tablet: `@media all and (min-width: 767px) and (max-width: 1023px)`,
    desktop: `@media all and (min-width: 1023px)`,
};

const theme = {
    lightColor,
    darkColor,
    fontSizes,
    paddings,
    margins,
    deviceSizes,
};

export default theme;
