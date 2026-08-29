import { apiClient } from "./client";
import type { CustomerRegisterPayload, TokenResponse } from "./types";

export async function registerCustomer(payload: CustomerRegisterPayload): Promise<void> {
  await apiClient.post("/auth/register/customer", payload);
}

export async function loginCustomer(username: string, password: string): Promise<TokenResponse> {
  const { data } = await apiClient.post<TokenResponse>("/auth/login/customer", {
    username,
    password,
  });
  return data;
}

export async function loginStaff(username: string, password: string): Promise<TokenResponse> {
  const { data } = await apiClient.post<TokenResponse>("/auth/login/staff", {
    username,
    password,
  });
  return data;
}
