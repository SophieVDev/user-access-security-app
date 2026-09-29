import { Component, inject } from '@angular/core';
import { Router } from '@angular/router';

import { AuthService } from '../../services/auth';

@Component({
  selector: 'app-dashboard',
  imports: [],
  templateUrl: './dashboard.html',
  styleUrl: './dashboard.scss',
})
export class Dashboard {
  private authService = inject(AuthService);
  private router = inject(Router);

  email = '';
  role = '';

  ngOnInit(): void {
    this.authService.getCurrentUser().subscribe({
      next: (user: any) => {
        this.email = user.email;
        this.role = user.role;
      },
      error: (error) => {
        console.error(
          'Erreur lors de la récupération de l’utilisateur :',
          error
        );
      },
    });
  }

  logout(): void {
    this.authService.logout();
    this.router.navigate(['/login']);
  }
}