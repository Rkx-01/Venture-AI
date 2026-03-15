import {
    LayoutDashboard,
    Lightbulb,
    BarChart3,
    Users,
    Zap,
    FileText,
    Settings,
    Search,
    Bell,
    Menu,
    ChevronLeft,
    ChevronRight,
    TrendingUp
} from "lucide-react";

export const DASHBOARD_NAV_ITEMS = [
    {
        label: "Dashboard",
        icon: LayoutDashboard,
        href: "/dashboard",
    },
    {
        label: "Analyze Idea",
        icon: Lightbulb,
        href: "/analyze",
    },
    {
        label: "Market Insights",
        icon: TrendingUp,
        href: "/market-insights",
    },
    {
        label: "Competitor Analysis",
        icon: Users,
        href: "/competitors",
    },
    {
        label: "Startup Score",
        icon: Zap,
        href: "/score",
    },
    {
        label: "Reports",
        icon: FileText,
        href: "/reports",
    },
];

export const SETTINGS_NAV_ITEM = {
    label: "Settings",
    icon: Settings,
    href: "/settings",
};
