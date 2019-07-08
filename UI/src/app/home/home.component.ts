import { Component } from '@angular/core';
import { first } from 'rxjs/operators';

import { User } from '@app/models/user';
import { UserService } from '@app/services/user.service';


@Component({ templateUrl: 'home.component.html' })
export class HomeComponent {
    loading = false;
    users: User[];

    constructor(private userService: UserService) { }

// tslint:disable-next-line: use-lifecycle-interface
    ngOnInit() {
        this.loading = true;
        this.userService.getAll().pipe(first()).subscribe(users => {
            this.loading = false;
            this.users = users;
        });
    }
}
