// =========================
// CUSTOMER TOKEN
// =========================
export function setCustomerToken(access: string, refresh: string) {
  if (typeof window === 'undefined') return;
  localStorage.setItem('customer_access_token', access);
}

export function getCustomerToken() {
  if (typeof window === 'undefined') return null;
  return localStorage.getItem('customer_access_token');
}

export function clearCustomerTokens() {
  if (typeof window === 'undefined') return;
  localStorage.removeItem('customer_access_token');
  // localStorage.removeItem('refreshToken');
}

// =========================
// Staff TOKEN
// =========================

export function setStaffToken(access: string, refresh: string) {
  if (typeof window === 'undefined') return;
  localStorage.setItem('staff_access_token', access);
}
export function getStaffToken() {
  if (typeof window === 'undefined') return null;
  return localStorage.getItem('staff_access_token');
}

export function clearStaffTokens() {
  if (typeof window === 'undefined') return;
  localStorage.removeItem('staff_access_token');
  // localStorage.removeItem('refreshToken');
}

// =========================
// Admin TOKEN
// =========================

export function setAdminToken(access: string, refresh: string) {
  if (typeof window === 'undefined') return;
  localStorage.setItem('admin_access_token', access);
}
export function getAdminToken() {
  if (typeof window === 'undefined') return null;
  return localStorage.getItem('admin_access_token');
}

export function clearAdminTokens() {
  if (typeof window === 'undefined') return;
  localStorage.removeItem('admin_access_token');
}

// =========================
// UNIVERSAL LOGOUT HANDLERS
// =========================

export function logoutCustomer() {
  clearCustomerTokens();
  if (typeof window !== 'undefined') window.location.href = '/auth/login';
}

export function logoutStaff() {
  clearStaffTokens();
  if (typeof window !== 'undefined') window.location.href = '/staff/auth/login';
}

export function logoutAdmin() {
  clearStaffTokens();
  if (typeof window !== 'undefined') window.location.href = '/admin/auth/login';
}
