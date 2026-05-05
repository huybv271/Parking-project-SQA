// ======================
// ROLE
// ======================
export type UserRole = 'customer' | 'staff' | 'admin';

// ======================
// BASE USER
// ======================
export interface BaseUser {
  username: string;
  role: UserRole;
  status?: boolean | number;
}

// ======================
// CUSTOMER USER
// ======================
export interface CustomerUser extends BaseUser {
  role: 'customer';
  gmail: string;
  verified: boolean;
}

// ======================
// STAFF USER (BAO GỒM ADMIN)
// ======================
export interface StaffUser extends BaseUser {
  role: 'staff' | 'admin';
  name?: string;
  date?: string;
}

// ======================
// AUTH PAYLOAD
// ======================
export interface LoginData {
  username: string;
  password: string;
}

// ======================
// LOGIN RESPONSES
// ======================

// CUSTOMER login
export interface CustomerLoginResponse {
  message: string;
  token: string;
  role: 'customer';
}

// STAFF + ADMIN login (dùng chung)
export interface StaffLoginResponse {
  message: string;
  token: string;
  role: 'staff' | 'admin';
}

// ====================== // REGISTER CUSTOMER // ======================
export interface RegisterData {
  username: string;
  password: string;
  gmail: string;
}
// ======================
// INFO RESPONSES
// ======================

// /user/infor
export interface CustomerInfoResponse {
  message: string;
  user: CustomerUser;
}

// /staff/infor (staff + admin đều trả staff)
export interface StaffInfoResponse {
  message: string;
  staff: StaffUser;
}

// ======================
// COMMON RESPONSES
// ======================
export interface RegisterResponse {
  message: string;
}

export interface VerifyEmailResponse {
  message: string;
}

export interface ResendVerifyResponse {
  message: string;
}

export interface ResetPasswordResponse {
  message: string;
}

export interface SendBarcodeResponse {
  message: string;
}

// ======================
// TYPE GUARDS
// ======================
export const isCustomer = (u: BaseUser): u is CustomerUser => u.role === 'customer';

export const isStaff = (u: BaseUser): u is StaffUser => u.role === 'staff' || u.role === 'admin';

export const isAdmin = (u: BaseUser): boolean => u.role === 'admin';
