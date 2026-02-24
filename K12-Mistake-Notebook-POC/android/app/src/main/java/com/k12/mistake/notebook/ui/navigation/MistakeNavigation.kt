package com.k12.mistake.notebook.ui.navigation

import androidx.compose.runtime.Composable
import androidx.navigation.NavHostController
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import com.k12.mistake.notebook.ui.camera.CameraScreen
import com.k12.mistake.notebook.ui.home.HomeScreen
import com.k12.mistake.notebook.ui.organize.OrganizeScreen
import com.k12.mistake.notebook.ui.save.SaveScreen
import com.k12.mistake.notebook.ui.selection.SelectionScreen

sealed class Screen(val route: String) {
    object Home : Screen("home")
    object Camera : Screen("camera")
    object Selection : Screen("selection")
    object Save : Screen("save")
    object Organize : Screen("organize")
}

@Composable
fun MistakeNavigation(
    navController: NavHostController = rememberNavController()
) {
    NavHost(
        navController = navController,
        startDestination = Screen.Home.route
    ) {
        // 主页
        composable(Screen.Home.route) {
            HomeScreen(
                onNavigateToCamera = {
                    navController.navigate(Screen.Camera.route)
                },
                onNavigateToOrganize = {
                    navController.navigate(Screen.Organize.route)
                }
            )
        }

        // 拍照页面
        composable(Screen.Camera.route) {
            CameraScreen(
                onPhotoTaken = { uri ->
                    navController.navigate(Screen.Selection.route)
                },
                onNavigateBack = {
                    navController.popBackStack()
                }
            )
        }

        // 选题页面
        composable(Screen.Selection.route) {
            SelectionScreen(
                onSelectionComplete = {
                    navController.navigate(Screen.Save.route)
                },
                onNavigateBack = {
                    navController.popBackStack()
                }
            )
        }

        // 保存页面
        composable(Screen.Save.route) {
            SaveScreen(
                onSaveComplete = {
                    navController.popUntil(Screen.Home.route)
                },
                onNavigateBack = {
                    navController.popBackStack()
                }
            )
        }

        // 组题页面
        composable(Screen.Organize.route) {
            OrganizeScreen(
                onNavigateBack = {
                    navController.popBackStack()
                }
            )
        }
    }
}
