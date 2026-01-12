from django.core.management.base import BaseCommand

from answers.models import Answer


class Command(BaseCommand):
    help = (
        "Migrate data from deprecated period and actual fields "
        "to new month, year and status fields"
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--force",
            action="store_true",
            help="Skip confirmation and execute migration",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show what would be done without executing",
        )
        parser.add_argument(
            "--limit",
            type=int,
            default=0,
            help="Limit number of records to process (for testing)",
        )
        parser.add_argument(
            "--skip-periods",
            action="store_true",
            help="Skip migration of period data (only migrate status)",
        )
        parser.add_argument(
            "--skip-status",
            action="store_true",
            help="Skip migration of status data (only migrate periods)",
        )

    def handle(self, *args, **options):
        force = options["force"]
        dry_run = options["dry_run"]
        limit = options["limit"]
        skip_periods = options["skip_periods"]
        skip_status = options["skip_status"]

        # Get answers for migration
        answers = Answer.objects.all().select_related("period")

        if limit:
            answers = answers[:limit]

        total_count = answers.count()
        migrated_count = 0
        skipped_count = 0
        errors = []

        self.stdout.write("\n" + "=" * 60)
        self.stdout.write("MIGRATION FROM DEPRECATED FIELDS")
        self.stdout.write("=" * 60)

        # Show statistics
        self.stdout.write(f"\nTotal answers: {total_count}")
        period_count = answers.filter(period__isnull=False).count()
        self.stdout.write(f"With Period relation: {period_count}")
        month_count = answers.exclude(month__isnull=True).count()
        self.stdout.write(f"Month field populated: {month_count}")
        year_count = answers.exclude(year__isnull=True).count()
        self.stdout.write(f"Year field populated: {year_count}")

        # Check for data conflicts
        conflicts = answers.filter(
            period__isnull=False, month__isnull=False, year__isnull=False
        ).count()

        if conflicts > 0 and not force:
            self.stdout.write(
                self.style.WARNING(
                    f"\nWARNING: {conflicts} records already have "
                    "month and year fields populated."
                )
            )
            self.stdout.write(
                "Migration will overwrite this data with values from "
                "deprecated fields."
            )

        # Confirm action
        if not force and not dry_run:
            confirm = input(
                "\nAre you sure you want to proceed with migration? (yes/no): "
            )
            if confirm.lower() != "yes":
                self.stdout.write(self.style.WARNING("Migration cancelled."))
                return

        if dry_run:
            self.stdout.write("\nDRY RUN MODE: No changes will be saved")
            self.stdout.write("Showing what WOULD be migrated:\n")
        else:
            self.stdout.write("\nEXECUTING MIGRATION...")

        # Process each record
        for i, answer in enumerate(answers, 1):
            try:
                would_update = False

                # Migrate period data (period -> month, year)
                if not skip_periods and answer.period and answer.period.period:
                    old_month = answer.month
                    old_year = answer.year

                    new_month = answer.period.period.month
                    new_year = answer.period.period.year

                    # Check if update is needed
                    if answer.month != new_month or answer.year != new_year:
                        would_update = True

                        # Log the change
                        if old_month and old_year:
                            self.stdout.write(
                                f"{i}. ID {answer.id}: Period "
                                f"{old_month}/{old_year} "
                                f"-> {new_month}/{new_year}"
                            )
                        else:
                            self.stdout.write(
                                f"{i}. ID {answer.id}: Would add period "
                                f"{new_month}/{new_year} from {answer.period}"
                            )

                        # Actually update if not dry run
                        if not dry_run:
                            answer.month = new_month
                            answer.year = new_year

                # Migrate status data (actual -> status)
                if not skip_status and answer.actual is not None:
                    # Convert Boolean to status - FIXED LOGIC
                    # actual=True -> STATUS_ACTUAL
                    # actual=False -> STATUS_OUTDATED
                    # actual=None -> keep existing status (don't migrate)
                    if answer.actual is True:
                        new_status = Answer.STATUS_ACTUAL
                    elif answer.actual is False:
                        new_status = Answer.STATUS_OUTDATED
                    else:
                        # actual is None, skip migration
                        continue

                    if answer.status != new_status:
                        would_update = True

                        self.stdout.write(
                            f"{i}. ID {answer.id}: Status "
                            f"'{answer.status}' -> '{new_status}' "
                            f"(from actual={answer.actual})"
                        )

                        # Actually update if not dry run
                        if not dry_run:
                            answer.status = new_status

                # Save if there were changes
                if would_update:
                    if not dry_run:
                        answer.save()
                        migrated_count += 1
                    else:
                        # In dry-run, count what WOULD be migrated
                        migrated_count += 1
                else:
                    skipped_count += 1

            except Exception as e:
                errors.append(f"ID {answer.id}: {str(e)}")
                self.stdout.write(
                    self.style.ERROR(
                        f"Error in record ID {answer.id}: {str(e)}"
                    )
                )

        # Show summary
        self.stdout.write("\n" + "=" * 60)
        self.stdout.write("MIGRATION SUMMARY")
        self.stdout.write("=" * 60)

        if dry_run:
            self.stdout.write(f"Would update records: {migrated_count}")
            self.stdout.write(f"Would skip records: {skipped_count}")
        else:
            self.stdout.write(f"Updated records: {migrated_count}")
            self.stdout.write(f"Skipped records: {skipped_count}")

        if errors:
            self.stdout.write(self.style.ERROR(f"\nErrors: {len(errors)}"))
            for error in errors[:10]:
                self.stdout.write(self.style.ERROR(f"  {error}"))
            if len(errors) > 10:
                self.stdout.write(
                    self.style.ERROR(
                        f"  ... and {len(errors) - 10} more errors"
                    )
                )
        else:
            self.stdout.write(self.style.SUCCESS("\nNo errors!"))

        if dry_run:
            self.stdout.write(
                self.style.WARNING(
                    "\nThis was a dry run. To execute migration "
                    "run the command without --dry-run flag"
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS("\nMigration completed successfully!")
            )

        # Show recommendations
        if migrated_count > 0:
            self.stdout.write("\n" + "-" * 60)
            self.stdout.write("RECOMMENDATIONS:")
            self.stdout.write("-" * 60)

            if not skip_periods:
                period_migrated = (
                    answers.filter(period__isnull=False)
                    .exclude(month__isnull=True, year__isnull=True)
                    .count()
                )

                if period_migrated > 0:
                    self.stdout.write(
                        f"1. {period_migrated} period records were migrated."
                    )
                    self.stdout.write(
                        "   You can now safely remove the 'period' field "
                        "from Answer model when ready."
                    )

            if not skip_status:
                status_migrated = answers.filter(actual__isnull=False).count()

                if status_migrated > 0:
                    self.stdout.write(
                        f"2. {status_migrated} status records were migrated."
                    )
                    self.stdout.write(
                        "   You can now safely remove the 'actual' field "
                        "from Answer model when ready."
                    )
