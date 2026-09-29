import { Injectable, inject } from '@angular/core';

import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  private http = inject(HttpClient);

  private apiUrl = 'http://127.0.0.1:8000';

  login(email: string, password: string) {
    return this.http.post(`${this.apiUrl}/login`, {
      email,
      password,
    });
  }

  getToken(): string | null {
    return sessionStorage.getItem('access_token');
  }

  getCurrentUser() {
    return this.http.get(`${this.apiUrl}/users/me`);
  }

  getAdminArea() {
    return this.http.get(`${this.apiUrl}/admin`);
  }

  logout(): void {
    sessionStorage.removeItem('access_token');
  }
}