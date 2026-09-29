import { Component, inject } from '@angular/core';
import { Router } from '@angular/router';

import {
  FormControl,
  FormGroup,
  ReactiveFormsModule,
  Validators,
} from '@angular/forms';

import { AuthService } from '../../services/auth';

@Component({
  imports: [ReactiveFormsModule],
  selector: 'app-login',
  styleUrl: './login.scss',
  templateUrl: './login.html',
})
export class Login {
  private authService = inject(AuthService);
  private router = inject(Router);

  message = '';
  currentUser = '';

  loginForm = new FormGroup({
    email: new FormControl('', [
      Validators.required,
      Validators.email,
    ]),
    password: new FormControl('', [
      Validators.required,
    ]),
  });

  onSubmit(): void {
    if (this.loginForm.invalid) {
      this.loginForm.markAllAsTouched();
      return;
    }

    this.message = '';
    this.currentUser = '';

    const email = this.loginForm.value.email!;
    const password = this.loginForm.value.password!;

    this.authService.login(email, password).subscribe({
      next: (response: any) => {
        this.message = response.message;

        if (response.access_token) {
          sessionStorage.setItem(
            'access_token',
            response.access_token
          );

          this.authService.getCurrentUser().subscribe({
            next: (user: any) => {
              this.currentUser = user.email;

              this.router.navigate(['/dashboard']);
            },
            error: (error) => {
              console.error(
                'Erreur lors de la récupération de l’utilisateur :',
                error
              );
            },
          });
        }
      },
      error: (error) => {
        if (error.status === 401) {
          this.message = 'Identifiants incorrects.';
          return;
        }

        this.message =
          'Une erreur est survenue. Veuillez réessayer.';
      },
    });
  }
}