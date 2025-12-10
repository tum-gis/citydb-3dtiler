def check_arguments(args):
    if args.style_mode == 'not-specified' and args.style_absence_behavior != 'not-specified':
        print("WARNING: You skipped specifying the style mode. The application will automatically select the 'objectclass-based' style mode.")
        return 1
    elif args.style_mode is None and args.style_absence_behavior is None:
        return 1
    else:
        return 1